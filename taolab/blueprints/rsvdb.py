from flask import render_template, abort, Blueprint, request, jsonify,flash,redirect,url_for
from jinja2 import TemplateNotFound
from taolab.ajax.rsvdbAJAX import *
import re

rsvdb = Blueprint("rsvdb", __name__)


@rsvdb.context_processor
def imspecies():
    spes = ["Arabidopsis", "Drosophila", "E.coli",
        "Human", "Mouse", "Rice", "Yeast", "Zebrafish"]
    return dict(spes=spes)

@rsvdb.route("/", defaults={'spin': 'Arabidopsis'})
@rsvdb.route("/browse", defaults={'spin': 'Arabidopsis'})
@rsvdb.route("/browse/<spin>", methods=['GET','POST'])
def showDetail(spin):
    from taolab.models import Species, SRRinfo, GSEinfo, Top100,RPKMhist,GiniBox,GiniHist
    if (request.method == 'POST'):
        if (request.values['med'] == 'geoname'):
            return ",".join(getGSE(Species, spin))
        elif (request.values['med'] == 'geoinfo'):
            tinfo = getGEOinfo(SRRinfo, GSEinfo, request.values['label'])
            return jsonify(tinfo)
        elif (request.values['med'] == 'srrtitle'):
            srrtitle = getSRRtitle(SRRinfo, request.values['label'],request.values['spe'])
            return jsonify(srrtitle)
        elif (request.values['med'] == 'srrinfo'):
            sinfo = getSRRinfo(SRRinfo, request.values['label'])
            return jsonify(sinfo)
        elif (request.values['med'] == 'srrstatic'):
            info = getSRRstatic(SRRinfo, request.values['label'])
            return jsonify(info)
        elif (request.values['med']=='samples'):
            infos=getSamples(SRRinfo,request.values['label'],request.values['spe'])
            return jsonify(infos)
        elif (request.values['med']=='top100'):
            topp=getTop100(Top100,request.values['label'])
            return (jsonify(topp))
        elif (request.values['med']=='rpkm'):
            rpkm=getRPKMhist(SRRinfo,RPKMhist,GiniBox,request.values['label'],request.values['spe'])
            return (jsonify(rpkm))
        elif (request.values['med']=='ginibox'):
            ginibox=getGiniBox(SRRinfo,RPKMhist,GiniBox,request.values['label'],request.values['spe'],request.values['thre'])
            return (jsonify(ginibox))
        elif (request.values['med']=='ginihist'):
            ginihist=getGiniHist(GiniHist,request.values['label'],request.values['thre'])
            return (jsonify(ginihist))
        else:
            return "You kidding..."
    elif (request.method == 'GET'):
        geo=request.args.get("geo")
        return render_template('rsvdb/browse.html', spin=spin,geo=geo)

    try:
        return render_template('rsvdb/browse.html', spin=spin,geo="DEF")
    except TemplateNotFound:
        abort(404)

@rsvdb.route("/viewer/", methods=['GET','POST'])
def showStruViewer():
    from taolab.models import Species,DMSTrans,GeneInfo,GeneSearch,Example,UTRinfo
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
            exa=getEamples(request.values['label'],Example)
            return jsonify(exa)
        elif(request.values['med']=='getstructure'):
            stru=getStructure(request.values['label'],request.values['dms'])
            return jsonify(stru)
        else:
            return "You kidding again..."
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
                return render_template('rsvdb/viewer.html',spe="Arabidopsis")
            except TemplateNotFound:
                abort(404)

@rsvdb.route("/support")
def showSupport():
    try:
        return render_template('rsvdb/support.html')
    except TemplateNotFound:
        abort(404)
