from taolab import rdb

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
    dms=rdb.Column(rdb.Integer)
    gini=rdb.Column(rdb.Float)
    rpkm=rdb.Column(rdb.Float)

class Example(rdb.Model):
    id=rdb.Column(rdb.Integer,primary_key=True)
    spe=rdb.Column(rdb.String(15))
    geneid=rdb.Column(rdb.String(20))
    genename=rdb.Column(rdb.String(30))

class RPKMhist(rdb.Model):
    id=rdb.Column(rdb.Integer,primary_key=True)
    simname=rdb.Column(rdb.String(50),index=True)
    # mid=rdb.Column(rdb.Text)
    rpkm=rdb.Column(rdb.Text)

class GiniBox(rdb.Model):
    id=rdb.Column(rdb.Integer,primary_key=True)
    simname=rdb.Column(rdb.String(50),index=True)
    thre=rdb.Column(rdb.Integer)
    five=rdb.Column(rdb.Text)
    cds=rdb.Column(rdb.Text)
    three=rdb.Column(rdb.Text)

class GiniHist(rdb.Model):
    id=rdb.Column(rdb.Integer,primary_key=True)
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