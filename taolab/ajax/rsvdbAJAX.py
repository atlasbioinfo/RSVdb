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
       
def getStructure(seq,dms):
    import os,time
    ctime=str(time.time())
    dmsarr=dms.split(";")
    with open("./Database/Temp/seq2"+ctime,'w') as f1:
        f1.write(seq)

    for ts in range(len(seq)):
        if (seq[ts]=="G" or seq[ts]=="T"):
            dmsarr[ts]=-999

    with open("./Database/Temp/dms2"+ctime,'w') as f2:
        for i in range(len(dmsarr)):
            f2.write(str(i+1)+'\t'+str(dmsarr[i])+"\n")
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
    fiveh=hlist.five.split(";")
    cdsh=hlist.cds.split(";")
    threeh=hlist.three.split(";")
    return {'fiveh':fiveh,'cdsh':cdsh,'threeh':threeh}

def getGiniBox(SRRinfo,RPKMhist,GiniBox,geo,spe,thre):
    if (thre=='auto'):
        thre=100
    else:
        thre=thre[:-1]
    slist=SRRinfo.query.filter(SRRinfo.geo==geo,SRRinfo.spe==spe).with_entities(SRRinfo.simsample).all()
    sample=set()
    for i in slist:
        sample.add(i.simsample)
    five=[]
    cds=[]
    three=[]
    sample=list(sample)
    for s in sample:
        gini=GiniBox.query.filter(GiniBox.simname==s,GiniBox.thre==thre).first()
        tfive=gini.five.split(";")
        tcds=gini.cds.split(";")
        tthree=gini.three.split(";")
        five.append(tfive)
        cds.append(tcds)
        three.append(tthree)

    return {'name':sample,'five':five,'cds':cds,'three':three,'thre':thre}

def getRPKMhist(SRRinfo,RPKMhist,GiniBox,geo,spe):
    slist=SRRinfo.query.filter(SRRinfo.geo==geo,SRRinfo.spe==spe).with_entities(SRRinfo.simsample).all()
    sample=set()
    for i in slist:
        sample.add(i.simsample)
    count=[]
    five=[]
    cds=[]
    three=[]
    sample=list(sample)
    thre=100        
    for s in sample:
        rpkm=RPKMhist.query.filter_by(simname=s).first()
        gini=GiniBox.query.filter(GiniBox.simname==s,GiniBox.thre==thre).first()
        tcount=rpkm.rpkm.split(";")
        tfive=gini.five.split(";")
        tcds=gini.cds.split(";")
        tthree=gini.three.split(";")
        count.append(tcount)
        five.append(tfive)
        cds.append(tcds)
        three.append(tthree)

    return {'count':count,'name':sample,'five':five,'cds':cds,'three':three}

def getTop100(Top100,srr):
    tlist=Top100.query.filter_by(srr=srr).all()
    total=len(tlist)
    rows=[]
    index=1
    for t in tlist:
        tmp={"id":index,"gene":t.gene,"length":t.length,"gc":round(float(t.gc),2),"dms":t.dms,"gini":round(float(t.gini),2),"rpkm":round(float(t.rpkm),2)}
        rows.append(tmp)
        index+=1
    return {"total":total,"rows":rows}

def getSamples(SRRinfo,geo,spe):
    slist=SRRinfo.query.filter(SRRinfo.geo==geo,SRRinfo.spe==spe).all()
    sample=[]
    for i in slist:
        sample.append(i.simsample)
    sample=list(set(sample))
    simname=[]
    name=[]
    srrstrlist=[]
    for s in sample:
        tsrr=SRRinfo.query.filter_by(simsample=s).all()
        srrlist=""
        for t in tsrr:
            srrlist=t.srr+","+srrlist
        srrlist=srrlist.strip(',')
        srrstrlist.append(srrlist)
        simname.append(s)
        tt=tsrr.pop()
        name.append(tt.sample)
    return {"simname":simname,"fullname":name,"srrstrlist":srrstrlist}

def getSRRstatic(SRRinfo, title):
    info = SRRinfo.query.filter_by(simsample=title).all()
    name = []
    ntm = []
    ntu = []
    ngm = []
    ngu = []
    for tmp in info:
        name.append(tmp.srr)
        ntm.append(tmp.mt)
        ntu.append(tmp.umt)
        ngm.append(tmp.mg)
        ngu.append(tmp.umg)
    return {"name": name, "ntm": ntm,"ntu":ntu,"ngm": ngm,"ngu":ngu}


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
    tmp=[]
    for i in info:
        tmp.append(i.srr)
    srrlist=",".join(tmp)
    finfo=info.pop()
    return {"srrlist": srrlist, "instru":finfo.instrument,"sample":finfo.sample,"runs":finfo.runs,"protocal":finfo.protocal}


def getGEOinfo(SRRinfo, GSEinfo, geo):
    info = GSEinfo.query.filter_by(geo=geo).first()
    srr=SRRinfo.query.filter_by(geo=geo).all()
    srrlist=[tmp.srr for tmp in srr]

    return {"geo": info.geo,"ref":srr[0].ref,'reflink':srr[0].reflink, "geolink":info.geolink,"title":info.title,"pmid":info.pmid,"summary":info.summary,"publicon":info.publicon,'srrlist':srrlist}


def getGSE(Species, spin):
    gse = Species.query.filter_by(gename=spin).with_entities(Species.geo).all()
    agse = [tmp.geo for tmp in gse]
    return agse

def getEamples(spe,Example):
    # print(spe)
    exa=Example.query.filter_by(spe=spe).first()
    # print(exa)
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
        gini=[]
        for s in seq:
            if ((s == "A") or (s == "C")):
                gini.append(1)
            else:
                gini.append(0)
            nseq.append(s+str(index))
            index+=1
        dms=[]
        simname=[]
        for d in dmsinfosearch:
            dms.append(d.dms.split(";"))
            simname.append(d.simname)
        return {"dms":dms,"simname":simname,"seq":nseq,'five':utr.five,'cds':utr.cds,'three':utr.three,'gini':gini}
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
    from taolab.models import Species
    astu = Species.query.filter_by(gename=name).all()
    tastu = [tmp.geo for tmp in astu]
    return tastu