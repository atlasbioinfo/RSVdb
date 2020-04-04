from flask import Flask, render_template, abort, Blueprint, request, jsonify,flash,redirect,url_for
from flask_sqlalchemy import SQLAlchemy
import click,os,sys,re

# Are you shocked by the 767 lines of 'app.py'?
# Actually, me too...
# For the production release, I of course split the code with "blueprint" and different packages.
# I originally wanted to use blueprint here, but always got feedback that the page was abnormal due to environmental issues.
# I used to adopt "Pipenv", but there were always some strange issues, such as python version conflicts and all packages being updated.
# So I ended up merging the code into an app.py.

# The advantage is: few scripts and easy to run!
# 1. Firstly, install python3
# 2. pip install flask flask-blueprint flask-sqlalchemy
# 3. flask run


def getLink(SEARCHlist,tinput):
    que=tinput.strip("")
    info = SEARCHlist.query.filter_by(que=que).first()
    if (info):
        return {"url":info.link}
    else:
        return {"url":"NULL"}

 

def doSearch(SEARCHlist,cinput):
    info = SEARCHlist.query.filter(SEARCHlist.que.ilike('%'+cinput+'%')).limit(10).all()
    res=[]
    if (info):
        tres=""
        tfamily=""
        for i in info:
            tres=i.que
            tfamily=i.family
            res.append({"res":tres,"family":tfamily})
        return {"res":res}
    else:
       return {"res":"NULL"}
       
def getStructure(seq,dms,thre,adj):
    import os,time
    ctime=str(time.time())
    dmsarr=dms.split(";")
    thre=float(thre)
    adj=float(adj)
    with open("./Database/Temp/seq2"+ctime,'w') as f1:
        f1.write(seq)

    for ts in range(len(seq)):
        dmsarr[ts]=float(dmsarr[ts])*adj
        if (seq[ts]=="G" or seq[ts]=="T"):
            dmsarr[ts]=-999
        if (dmsarr[ts]>thre):
            dmsarr[ts]=thre
        

    with open("./Database/Temp/dms2"+ctime,'w') as f2:
        for i in range(len(dmsarr)):
            # if (dmsarr[i]==0):
            #     dmsarr[i]=-999
            f2.write(str(i+1)+'\t'+str(dmsarr[i])+"\n")
    # os.system('Fold.exe Database/Temp/seq2'+ctime+' Database/Temp/out'+ctime+'.ct')
    # os.system('ct2dot.exe Database/Temp/out'+ctime+'.ct 1 Database/Temp/out2'+ctime+'.dot')
    os.system('Fold Database/Temp/seq2'+ctime+' Database/Temp/out'+ctime+'.ct')
    os.system('ct2dot Database/Temp/out'+ctime+'.ct 1 Database/Temp/out2'+ctime+'.dot')
    vitromfe=0
    vitrodot=''
    vivomfe=0
    vivodot=''
    with open('./Database/Temp/out2'+ctime+'.dot', 'r') as file:
        r=file.readlines()
        if (len(r[0].split())>2):
            vitromfe=r[0].split()[2]
        else:
            vitromfe="None"
        vitrodot=r[2].strip("\n")
    
    os.system('Fold Database/Temp/seq2'+ctime+' Database/Temp/out3'+ctime+'.ct -dms Database/Temp/dms2'+ctime)
    os.system('ct2dot Database/Temp/out3'+ctime+'.ct 1 Database/Temp/out4'+ctime+'.dot')
    # os.system('Fold.exe Database/Temp/seq2'+ctime+' Database/Temp/out3'+ctime+'.ct -dms Database/Temp/dms2'+ctime)
    # os.system('ct2dot.exe Database/Temp/out3'+ctime+'.ct 1 Database/Temp/out4'+ctime+'.dot')

    with open('./Database/Temp/out4'+ctime+'.dot', 'r') as file:
        r=file.readlines()
        if (len(r[0].split())>2):
            vivomfe=r[0].split()[2]
        else:
            vivomfe="None"
        
        vivodot=r[2].strip("\n")
    os.system('rm Database/Temp/seq2'+ctime+' Database/Temp/dms2'+ctime+' Database/Temp/out'+ctime+'.ct Database/Temp/out2'+ctime+'.dot Database/Temp/out3'+ctime+'.ct Database/Temp/out4'+ctime+'.dot')
    
    return {'vitromfe':vitromfe,'vitrodot':vitrodot,'vivomfe':vivomfe,'vivodot':vivodot}

def getGiniHist(GiniHist,simname,thre):
    if (thre=='auto'):
        thre=100
    else:
        thre=thre[:-1]
    hlist=GiniHist.query.filter(GiniHist.simname==simname,GiniHist.thre==thre).first()
    if (not hlist):
        return
    fiveh=hlist.five.split(";")
    cdsh=hlist.cds.split(";")
    threeh=hlist.three.split(";")
    return {'fiveh':fiveh,'cdsh':cdsh,'threeh':threeh}

def getGiniBox(GiniBox,geo,spe,thre):
    if (thre=='auto'):
        thre='0%'
    slist=GiniBox.query.filter(GiniBox.geo==geo,GiniBox.spe==spe,GiniBox.thre==thre).all()
    sample=set()
    five=[]
    cds=[]
    three=[]
    thre=[]
    for i in slist:
        sample.add(i.simname)
        five.append(i.five.split(";"))
        cds.append(i.cds.split(";"))
        three.append(i.three.split(";"))
    return {'name':list(sample),'five':five,'cds':cds,'three':three}

def getInterRef(InterRef,geo,spe):
    tinref=InterRef.query.filter(InterRef.geo==geo,InterRef.spe==spe).first()
    return {'transname':tinref.transname,'commonname':tinref.commonname,'meanr':tinref.meanr,'dis':tinref.dis}

def getRPKMhist(RPKMhist,DMSActHist,geo,spe):
    rpkmlist=RPKMhist.query.filter(RPKMhist.geo==geo,RPKMhist.spe==spe)
    count=[]
    tsample=[]
    tmax=rpkmlist[0].max
    for trpkm in rpkmlist:
        tsample.append(trpkm.simname)
        tcount=trpkm.rpkm
        count.append(tcount)
    
    tdms=DMSActHist.query.filter(DMSActHist.geo==geo,DMSActHist.spe==spe)
    dmscount=[]
    dmstsample=[]
    dmstmax=tdms[0].max
    dmstmin=tdms[0].min
    for tt in tdms:
        dmstsample.append(tt.simname)
        dmstcount=tt.dmshist
        dmscount.append(dmstcount)
    return {'count':count,'name':tsample,'max':tmax,'dmscount':dmscount,'dmsname':dmstsample,'dmsmax':dmstmax,'dmsmin':dmstmin}


def getTop100(Top100,srr):
    tlist=Top100.query.filter_by(srr=srr).all()
    total=len(tlist)
    rows=[]
    index=1
    for t in tlist:
        tmp={"id":index,"gene":t.gene,"length":t.length,"gc":str(round(float(t.gc),4)*100)+"%","acratio":t.acratio,"dms":t.dms,"gini":round(float(t.gini),2),"rpkm":round(float(t.rpkm),2)}
        rows.append(tmp)
        index+=1
    return {"total":total,"rows":rows}

def getCombineTop100(CombineTop100, simname):
    #this simname is combine name
    ctop=CombineTop100.query.filter(CombineTop100.simname==simname).all()
    total=len(ctop)
    rows=[]
    index=1
    for t in ctop:
        tmp={"id":index,"gene":t.gene,"length":t.length,"gc":str(round(float(t.gc),4)*100)+"%","dms":t.dms}
        rows.append(tmp)
        index+=1
        
    return {"total":total,"rows":rows}

def getSamples(SRRinfo,geo,spe):
    slist=SRRinfo.query.filter(SRRinfo.geo==geo,SRRinfo.spe==spe).all()
    ref=slist[0].ref
    reflink=slist[0].reflink
    biopro=slist[0].biopro
    runs=slist[0].runs
    instru=slist[0].instrument
    protocal=slist[0].protocal
    srrlist=[]
    samplename=[]
    simnamedict={}
    hebingdict={}
    for i in slist:
        srrlist.append(i.srr)
        samplename.append(i.sample)
        if (i.simsample in simnamedict):
            simnamedict[i.simsample]+=1
        else:
            simnamedict[i.simsample]=1
    
        if (i.hebingname in hebingdict):
            hebingdict[i.hebingname]+=1
        else:
            hebingdict[i.hebingname]=1
    rowspan=[]
    rowspanhebing=[]
    simname=[]
    hebingname=[]
    for i in slist:
        rowspan.append(simnamedict[i.simsample])
        rowspanhebing.append(hebingdict[i.hebingname])
        simname.append(i.simsample)
        hebingname.append(i.hebingname)
        simnamedict[i.simsample]=0
        hebingdict[i.hebingname]=0
  
    return {"simname":simname,"fullname":samplename,"rowspan":rowspan,"rowspanhebing":rowspanhebing,"hebingname":hebingname,"srrlist":srrlist,"ref":ref,"reflink":reflink,"biopro":biopro,"runs":runs,"instru":instru,"protocal":protocal}

def getMergeSamples(SRRinfo,geo,spe):
    slist=SRRinfo.query.filter(SRRinfo.geo==geo,SRRinfo.spe==spe).all()
    rowspan=[]
    simname=[]



def getSRRstatic(SRRinfo, geo, spe):
    info = SRRinfo.query.filter(SRRinfo.geo==geo,SRRinfo.spe==spe).all()
    srrname = []
    simsample=[]
    genomeMap={"map":list(),"unmap":list()}
    transMap={"map":list(),"unmap":list()}
    genomeATCG={"a":list(),"t":list(),"c":list(),"g":list()}
    transATCG={"a":list(),"t":list(),"c":list(),"g":list()}
    for t in info:
        srrname.append(t.srr)
        simsample.append(t.simsample)
        genomeMap['map'].append(t.mg)
        genomeMap['unmap'].append(t.umg)
        transMap['map'].append(t.mt)
        transMap['unmap'].append(t.umt)
        genomeATCG['a'].append(t.ag)
        genomeATCG['t'].append(t.tg)
        genomeATCG['c'].append(t.cg)
        genomeATCG['g'].append(t.gg)
        transATCG['a'].append(t.at)
        transATCG['t'].append(t.tt)
        transATCG['c'].append(t.ct)
        transATCG['g'].append(t.gt)
    return {"simsample":simsample,"srrname": srrname, "genomeMap":genomeMap,"transMap":transMap,"genomeATCG":genomeATCG,"transATCG":transATCG}


def getSRRtitle(SRRinfo, geo,spe):
    info = SRRinfo.query.filter(SRRinfo.geo==geo,SRRinfo.spe==spe).with_entities(SRRinfo.simsample).all()
    name=set()
    for tname in info:
        name.add(tname[0])
    name=list(name)

    ntm = []
    ntu = []
    ngm = []
    ngu = []
    at=[]
    ct=[]
    gt=[]
    tt=[]
    ag=[]
    cg=[]
    gg=[]
    tg=[]
    totalmu=[0,0,0,0]
    totalacgt=[0,0,0,0,0,0,0,0]

    for tmp in name:
        mapinfo=SRRinfo.query.filter_by(simsample=tmp).all()
        maparr=[0,0,0,0]
        mapacgt=[0,0,0,0,0,0,0,0]
        count=0
        for tmpp in mapinfo:
            count+=1
            maparr[0]+=float(tmpp.mt)
            maparr[1]+=float(tmpp.umt)
            maparr[2]+=float(tmpp.mg)
            maparr[3]+=float(tmpp.umg)
            mapacgt[0]+=float(tmpp.at)
            mapacgt[1]+=float(tmpp.ct)
            mapacgt[2]+=float(tmpp.gt)
            mapacgt[3]+=float(tmpp.tt)
            mapacgt[4]+=float(tmpp.ag)
            mapacgt[5]+=float(tmpp.cg)
            mapacgt[6]+=float(tmpp.gg)
            mapacgt[7]+=float(tmpp.tg)

        for m in range(len(maparr)):
            maparr[m]=maparr[m]/count
        for k in range(len(mapacgt)):
            mapacgt[k]=mapacgt[k]/count

        ntm.append(maparr[0])
        ntu.append(maparr[1])
        ngm.append(maparr[2])
        ngu.append(maparr[3])
        at.append(mapacgt[0])
        ct.append(mapacgt[1])
        gt.append(mapacgt[2])
        tt.append(mapacgt[3])
        ag.append(mapacgt[4])
        cg.append(mapacgt[5])
        gg.append(mapacgt[6])
        tg.append(mapacgt[7])

    for i in range(len(ntm)):
        totalmu[0]+=ntm[i]/(len(ntm))
        totalmu[1]+=ntu[i]/(len(ntm))
        totalmu[2]+=ngm[i]/(len(ntm))
        totalmu[3]+=ngu[i]/(len(ntm))
        totalacgt[0]+=at[i]/(len(ntm))
        totalacgt[1]+=ct[i]/(len(ntm))
        totalacgt[2]+=gt[i]/(len(ntm))
        totalacgt[3]+=tt[i]/(len(ntm))
        totalacgt[4]+=ag[i]/(len(ntm))
        totalacgt[5]+=cg[i]/(len(ntm))
        totalacgt[6]+=gg[i]/(len(ntm))
        totalacgt[7]+=tg[i]/(len(ntm))

    summu=totalmu[0]+totalmu[1]
    summug=totalmu[2]+totalmu[3]
    totalmu[0]=totalmu[0]/summu
    totalmu[1]=totalmu[1]/summu
    totalmu[2]=totalmu[2]/summug
    totalmu[3]=totalmu[3]/summug
    totalmu[0]=round(totalmu[0],3)
    totalmu[1]=round(totalmu[1],3)
    totalmu[2]=round(totalmu[2],3)
    totalmu[3]=round(totalmu[3],3)
    totalacgt[0]=round(totalacgt[0],3)
    totalacgt[1]=round(totalacgt[1],3)
    totalacgt[2]=round(totalacgt[2],3)
    totalacgt[3]=round(totalacgt[3],3)
    totalacgt[4]=round(totalacgt[4],3)
    totalacgt[5]=round(totalacgt[5],3)
    totalacgt[6]=round(totalacgt[6],3)
    totalacgt[7]=round(totalacgt[7],3)
    
    return {"name":name,"ntm": ntm,"ntu":ntu,"ngm": ngm,"ngu":ngu,"totalmu":totalmu,"totalacgt":totalacgt}


def getSRRinfo(SRRinfo, title):
    info = SRRinfo.query.filter_by(simsample=title).all()
    srrArr=[]
    sampleSet=set()
    runsSet=set()
    insSet=set()
    for i in info:
        srrArr.append(i.srr)
        sampleSet.add(i.sample)
        runsSet.add(i.runs)
        insSet.add(i.instrument)
    srrlist=",".join(srrArr)
    finfo=info.pop()
    return {"srrlist": srrlist, "instru":"<br />".join(insSet),"sample":"<br />".join(sampleSet),"runs":"<br />".join(runsSet),"protocal":finfo.protocal}

def getGEOinfo(SRRinfo, GSEinfo, geo):
    info = GSEinfo.query.filter_by(geo=geo).first()
    return {"geo": info.geo, "geolink":info.geolink,"title":info.title,"pmid":info.pmid,"summary":info.summary,"publicon":info.publicon,"ref":info.ref}

def getGEOinfo2(SRRinfo, GSEinfo, geo): 
    info = GSEinfo.query.filter_by(geo=geo).first()
    srr=SRRinfo.query.filter_by(geo=geo).all()
    srrlist=[tmp.srr for tmp in srr]
    return {"geo": info.geo,"ref":srr[0].ref,'reflink':srr[0].reflink, "geolink":info.geolink,"title":info.title,"pmid":info.pmid,"summary":info.summary,"publicon":info.publicon,'srrlist':srrlist}


def getGSE(Species, spin):
    gse = Species.query.filter_by(gename=spin).with_entities(Species.geo).all()
    agse = [tmp.geo for tmp in gse]
    return agse

def getEamples(spe,geo,Example):
    exa=Example.query.filter_by(spe=spe,geo=geo).first()
    return {"geneid":exa.geneid,"genename":exa.genename}

def getTrueId(search,GeneSearch,GeneInfo,spe):
    search=search.strip()
    isearch=GeneSearch.query.filter_by(geneid=search,spe=spe).first()
    nsearch=GeneSearch.query.filter_by(genename=search,spe=spe).first()
    geneid=""
    if (isearch):
        geneid=isearch.geneid
    elif(nsearch):
        geneid=nsearch.geneid
    else:
        return {'genetrueid':"None"}
    
    gsearch=GeneInfo.query.filter_by(transid=geneid,spe=spe).first()

    if (gsearch):
        return {'genetrueid':geneid,'commonname':gsearch.commonname,"genedis":gsearch.genedis,"gc":gsearch.gc,"genetype":gsearch.genetype,"chrom":gsearch.chrom}
    else:
        return {'genetrueid':geneid,'commonname':"None"}



def getDMSinfo(geo,genename,DMSTrans,UTRinfo):
    genename=genename.strip()
    # genename=genename.upper()
    dmsinfosearch=DMSTrans.query.filter_by(geo=geo,transid=genename).all()
    if (dmsinfosearch):
        utr=UTRinfo.query.filter_by(transid=genename).first()
        seq=dmsinfosearch[0].transseq
        index=1
        nseq=[]
        account=0
        for s in seq:
            if (re.match(r'A|C',s,re.I)):
                account+=1
            nseq.append(s+str(index))
            index+=1
        dms=[]
        ndms={}
        simname=[]
        count={}
        for d in dmsinfosearch:
            dmscount=0
            
            dmsarr=d.dms.split(";")
            tmparr=[]
            for i in range(len(dmsarr)):
                if (len(dmsarr[i])==0):
                    continue
                dmsarr[i]=float(dmsarr[i])
                tmparr.append(dmsarr[i])
                dmscount+=dmsarr[i]
            ndms[d.simname]=tmparr          
            dmscount=dmscount/account
            count[d.simname]=dmscount
        return {"dms":ndms,"seq":nseq,'five':utr.five,'cds':utr.cds,'three':utr.three,'count':count}
    else:
        return {"dms":"None"}

def searchGene(geo,spe,search,GeneSearch):
    glist=GeneSearch.query.filter(GeneSearch.geo==geo,GeneSearch.spe==spe,GeneSearch.geneid.ilike('%'+search+'%')).limit(5).all()
    nlist=GeneSearch.query.filter(GeneSearch.geo==geo,GeneSearch.spe==spe,GeneSearch.genename.ilike('%'+search+'%')).limit(5).all()
    tlist=[]
    tset=set()
    for g in glist:
        if (g.genename):
            addinfo=g.geneid+"-"+g.genename
        else:
            addinfo=g.geneid
        tset.add(addinfo)
    for n in nlist:
        addinfo2=n.geneid+"-"+n.genename
        tset.add(addinfo2)
    tlist=list(tset)
    return {"ajlist":tlist}

def getStudies(name):
    astu = Species.query.filter_by(gename=name).all()
    tastu = [tmp.geo for tmp in astu]
    return tastu

def getDownload(geo,spe,Download):
    tdown=Download.query.filter_by(geo=geo,spe=spe).all()
    count=0
    rows=[]
    for td in tdown:
        count+=1
        tdict={"id":count,"sample":td.simname,"trans":td.transc,"cov":td.cov,"dms":td.dms,"gini":td.gini,"download":""}
        rows.append(tdict)
    
    return {"total":count,"rows":rows}

def register_errors(app):
    @app.errorhandler(404)
    def pagenotfound(e):
        return render_template('rsvdb/404.html'), 404

def register_commands(app): 
    @app.cli.command()
    @click.option('--drop', is_flag=True, help="Creat after drop")
    def initdb(drop):
        if drop:
            rdb.drop_all()
        rdb.create_all()
        click.echo("Initialized db")

rsvdb = Flask(__name__)

WIN = sys.platform.startswith('win')
prefix=""
if WIN:
    prefix = 'sqlite:///'
else:
    prefix = 'sqlite:////'

rsvdb.config['SQLALCHEMY_DATABASE_URI']=prefix + os.path.join("./", './Database/data.db')
rsvdb.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

rdb = SQLAlchemy(rsvdb)

register_commands(rsvdb)
register_errors(rsvdb)
class Species(rdb.Model):
    id=rdb.Column(rdb.Integer, primary_key=True)
    name=rdb.Column(rdb.String(40))
    gename=rdb.Column(rdb.String(20))
    geo=rdb.Column(rdb.String(15))

class GSEinfo(rdb.Model):
    id=rdb.Column(rdb.Integer,primary_key=True)
    geo=rdb.Column(rdb.String(15),index=True)
    geolink=rdb.Column(rdb.String(120))
    title=rdb.Column(rdb.String(150))
    pmid=rdb.Column(rdb.Integer,nullable=True)
    summary=rdb.Column(rdb.Text)
    publicon=rdb.Column(rdb.String(15))
    ref=rdb.Column(rdb.Text)

class SRRinfo(rdb.Model):
    __tablename__ = 'srrinfo'
    id=rdb.Column(rdb.Integer,primary_key=True)
    srr=rdb.Column(rdb.String(10),unique=True)
    geo=rdb.Column(rdb.String(12),index=True)
    spe=rdb.Column(rdb.String(40),index=True)
    ref=rdb.Column(rdb.String(10))
    reflink=rdb.Column(rdb.Text)
    biopro=rdb.Column(rdb.String(12))
    sra=rdb.Column(rdb.String(12))
    srx=rdb.Column(rdb.String(12))
    sample=rdb.Column(rdb.String(100))
    simsample=rdb.Column(rdb.String(50),index=True)
    hebingname=rdb.Column(rdb.String(50),index=True)
    instrument=rdb.Column(rdb.String(100))
    runs=rdb.Column(rdb.String(100))
    submiter=rdb.Column(rdb.String(50))
    protocal=rdb.Column(rdb.Text)
    mt=rdb.Column(rdb.Float)
    umt=rdb.Column(rdb.Float)
    mg=rdb.Column(rdb.Float)
    umg=rdb.Column(rdb.Float)
    at=rdb.Column(rdb.Float)
    ct=rdb.Column(rdb.Float)
    gt=rdb.Column(rdb.Float)
    tt=rdb.Column(rdb.Float)
    ag=rdb.Column(rdb.Float)
    cg=rdb.Column(rdb.Float)
    gg=rdb.Column(rdb.Float)
    tg=rdb.Column(rdb.Float)

class SEARCHlist(rdb.Model):
    id=rdb.Column(rdb.Integer,primary_key=True)
    que=rdb.Column(rdb.String(60,collation='NOCASE'), index=True)
    family=rdb.Column(rdb.String(20))
    link=rdb.Column(rdb.Text)

class DMSTrans(rdb.Model):
    __tablename__ ='dmstrans'
    id=rdb.Column(rdb.Integer,primary_key=True)
    geo=rdb.Column(rdb.String(12),index=True)
    simname=rdb.Column(rdb.String(50))
    transid=rdb.Column(rdb.String(30),index=True)
    transseq=rdb.Column(rdb.Text)
    dms=rdb.Column(rdb.Text)

class GeneInfo(rdb.Model):
    id=rdb.Column(rdb.Integer,primary_key=True)
    spe=rdb.Column(rdb.String(40),index=True)
    transid=rdb.Column(rdb.String(30),unique=True, index=True)
    commonname=rdb.Column(rdb.String(80),index=True)
    genedis=rdb.Column(rdb.Text)
    gc=rdb.Column(rdb.Float)
    genetype=rdb.Column(rdb.String(50))
    chrom=rdb.Column(rdb.String(20))

class GeneSearch(rdb.Model):
    id=rdb.Column(rdb.Integer,primary_key=True)
    geo=rdb.Column(rdb.String(12),index=True)
    spe=rdb.Column(rdb.String(15),index=True)
    geneid=rdb.Column(rdb.String(20),index=True)
    genename=rdb.Column(rdb.String(30,collation='NOCASE'),index=True)

class Top100(rdb.Model):
    id=rdb.Column(rdb.Integer,primary_key=True)
    srr=rdb.Column(rdb.String(10),index=True)
    gene=rdb.Column(rdb.String(30))
    length=rdb.Column(rdb.Integer)
    gc=rdb.Column(rdb.Float)
    acratio=rdb.Column(rdb.Float)
    dms=rdb.Column(rdb.Float)
    gini=rdb.Column(rdb.Float)
    rpkm=rdb.Column(rdb.Float)

class Download(rdb.Model):
    __tablename__ ='download'
    id=rdb.Column(rdb.Integer,primary_key=True)
    geo=rdb.Column(rdb.String(15),index=True)
    spe=rdb.Column(rdb.String(15))
    simname=rdb.Column(rdb.String(50))
    transc=rdb.Column(rdb.Integer)
    cov=rdb.Column(rdb.Float)
    dms=rdb.Column(rdb.Float)
    gini=rdb.Column(rdb.Float)
    

class CombineTop100(rdb.Model):
    __tablename__ ='combine_top100'
    id=rdb.Column(rdb.Integer,primary_key=True)
    geo=rdb.Column(rdb.String(15),index=True)
    simname=rdb.Column(rdb.String(50),index=True)
    gene=rdb.Column(rdb.String(30))
    length=rdb.Column(rdb.Integer)
    gc=rdb.Column(rdb.Float)
    dms=rdb.Column(rdb.Float)

class InterRef(rdb.Model):
    id=rdb.Column(rdb.Integer,primary_key=True)
    geo=rdb.Column(rdb.String(14))
    spe=rdb.Column(rdb.String(15),index=True)
    transname=rdb.Column(rdb.String(18))
    meanr=rdb.Column(rdb.Float)
    commonname=rdb.Column(rdb.String(16))
    dis=rdb.Column(rdb.Text)

class Example(rdb.Model):
    id=rdb.Column(rdb.Integer,primary_key=True)
    spe=rdb.Column(rdb.String(15))
    geo=rdb.Column(rdb.String(10))
    geneid=rdb.Column(rdb.String(20))
    genename=rdb.Column(rdb.String(30))

class RPKMhist(rdb.Model):
    id=rdb.Column(rdb.Integer,primary_key=True)
    geo=rdb.Column(rdb.String(10),index=True)
    spe=rdb.Column(rdb.String(15),index=True)
    simname=rdb.Column(rdb.String(50))
    max=rdb.Column(rdb.Float)
    rpkm=rdb.Column(rdb.Text)

class GiniBox(rdb.Model):
    __tablename__ ='gini_box'
    id=rdb.Column(rdb.Integer,primary_key=True)
    geo=rdb.Column(rdb.String(12),index=True)
    spe=rdb.Column(rdb.String(15))
    simname=rdb.Column(rdb.String(50))
    thre=rdb.Column(rdb.String(5))
    five=rdb.Column(rdb.Text)
    cds=rdb.Column(rdb.Text)
    three=rdb.Column(rdb.Text)

class GiniHist(rdb.Model):
    id=rdb.Column(rdb.Integer,primary_key=True)
    geo=rdb.Column(rdb.String(12),index=True)
    simname=rdb.Column(rdb.String(50),index=True)
    thre=rdb.Column(rdb.Integer)
    five=rdb.Column(rdb.Text)
    cds=rdb.Column(rdb.Text)
    three=rdb.Column(rdb.Text)

class UTRinfo(rdb.Model):
    id=rdb.Column(rdb.Integer,primary_key=True)
    transid=rdb.Column(rdb.String(30),index=True)
    five=rdb.Column(rdb.Integer)
    cds=rdb.Column(rdb.Integer)
    three=rdb.Column(rdb.Integer)

class DMSActHist(rdb.Model):
    __tablename__ ='dmsact_hist'
    id=rdb.Column(rdb.Integer,primary_key=True)
    geo=rdb.Column(rdb.String(12),index=True)
    spe=rdb.Column(rdb.String(15),index=True)
    simname=rdb.Column(rdb.String(50))
    min=rdb.Column(rdb.Float)
    max=rdb.Column(rdb.Float)
    dmshist=rdb.Column(rdb.Text)

@rsvdb.context_processor
def imspecies():
    spes = ["Arabidopsis", "Drosophila", "E.coli",
        "Human", "Mouse", "Rice", "Yeast", "Zebrafish"]
    return dict(spes=spes)

@rsvdb.route("/", defaults={'spin': 'Arabidopsis'})
@rsvdb.route("/<spin>", methods=['GET','POST'])
@rsvdb.route("/browse", defaults={'spin': 'Arabidopsis'})
@rsvdb.route("/browse/<spin>", methods=['GET','POST'])
def showDetail(spin):
    if (request.method == 'POST'):
        if (request.values['med'] == 'geoname'):
            return ",".join(getGSE(Species, spin))
        elif (request.values['med'] == 'geoinfo'):
            tinfo = getGEOinfo(SRRinfo, GSEinfo, request.values['label'])
            return jsonify(tinfo)
        elif (request.values['med'] == 'srrinfo'):
            sinfo = getSRRinfo(SRRinfo, request.values['label'])
            return jsonify(sinfo)
        elif (request.values['med'] == 'srrstatic'):
            info = getSRRstatic(SRRinfo, request.values['label'],request.values['spe'])
            return jsonify(info)
        elif (request.values['med']=='samples'):
            infos=getSamples(SRRinfo,request.values['label'],request.values['spe'])
            return jsonify(infos)
        elif (request.values['med']=='top100'):
            topp=getTop100(Top100,request.values['label'])
            return (jsonify(topp))
        elif (request.values['med']=='combinetop100'):
            ctopp=getCombineTop100(CombineTop100,request.values['label'])
            return (jsonify(ctopp))
        elif (request.values['med']=='interref'):
            tinterref=getInterRef(InterRef,request.values['geo'],request.values['spe'])
            return (jsonify(tinterref))
        elif (request.values['med']=='rpkm'):
            rpkm=getRPKMhist(RPKMhist,DMSActHist,request.values['label'],request.values['spe'])
            return (jsonify(rpkm))
        elif (request.values['med']=='ginibox'):
            ginibox=getGiniBox(GiniBox,request.values['label'],request.values['spe'],request.values['thre'])
            return (jsonify(ginibox))
        elif (request.values['med']=='ginihist'):
            ginihist=getGiniHist(GiniHist,request.values['label'],request.values['thre'])
            return (jsonify(ginihist))
        else:
            return "Request-values validation failed in Browse"
    elif (request.method == 'GET'):
        geo=request.args.get("geo")
        return render_template('rsvdb/browse.html', spin=spin,geo=geo)

    try:
        return render_template('rsvdb/browse.html', spin=spin,geo="DEF")
    except TemplateNotFound:
        abort(404)

@rsvdb.route("/viewer/", methods=['GET','POST'])
def showStruViewer():
    if (request.method == 'POST'):
        if (request.values['med'] == 'searchGene'):
            tlist=searchGene(request.values['geo'],request.values['spe'],request.values['label'], GeneSearch)
            return jsonify(tlist)
        elif (request.values['med'] == 'dmsinfo'):
            dmslist=getDMSinfo(request.values['geo'],request.values['label'], DMSTrans,UTRinfo)
            return jsonify(dmslist)
        elif(request.values['med']=='gettrueid'):
            genelist=getTrueId(request.values['label'],GeneSearch,GeneInfo,request.values['spe'])
            return jsonify(genelist)
        elif(request.values['med']=='Example'):
            exa=getEamples(request.values['label'],request.values['geo'],Example)
            return jsonify(exa)
        elif(request.values['med']=='getstructure'):
            stru=getStructure(request.values['label'],request.values['dms'],request.values['thre'],request.values['adj'])
            return jsonify(stru)
        else:
            return "Request-values validation failed in Viewer"
    elif (request.method == 'GET'):
        spe=request.args.get("spe")
        if (spe):
            geo=request.args.get("geo")
            gene=request.args.get("gene")
            try:
                return render_template('rsvdb/viewer.html',spe=spe,geo=geo,gene=gene)
            except TemplateNotFound:
                abort(404)
        else:
            try:
                return render_template('rsvdb/viewer.html',spe="Arabidopsis",geo="GSE108857")
            except TemplateNotFound:
                abort(404)


@rsvdb.route("/support")
def showSupport():
    try:
        return render_template('rsvdb/support.html')
    except TemplateNotFound:
        abort(404)
