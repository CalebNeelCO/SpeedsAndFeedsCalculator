import json
from flask import Flask, jsonify, render_template, request
app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template('index.html')

@app.route('/speedsandfeedsendpoint')
def calulatue():
    a = request.args.get('a', 0, type=int)
    b = request.args.get('b', 0, type=int)
    return jsonify(result=a + b)
  
materals = """{
  "Carbide": {
    "Aluminum 440, 356, 380, C61300": {
      "SFM": "500-1000",
      "IPM": {
        "1": 0.007,
        "0.125": 0.001,
        "0.1875": 0.002,
        "0.25": 0.002,
        "0.375": 0.003,
        "0.5": 0.004,
        "0.625": 0.005,
        "0.75": 0.006
      }
    }
  }
}"""
materals = json.loads(materals)


def getSFM(materal, endmilltype):
  sfm = materals[endmilltype][materal]["SFM"]
  sfm = sfm.split("-")
  return sfm

def getRMP(dia, sfm):
  RPM = (3.82*int(sfm))/dia
  return RPM
  
def getCL(dia,  materal, endmilltype):
  if(materals[endmilltype][materal]["IPM"][str(dia)] != None):
    return materals[endmilltype][materal]["IPM"][str(dia)]
  else:
    return False
  
def getSpeeds(dia, numOfTeeth, materal="", endmilltype="", sfm=0, CL = 0):
  speeds = []
  if(sfm != 0):
    sfm = [sfm]
  else:
    sfm = getSFM(materal, endmilltype)
  for x in range(len(sfm)):
    rpm = getRMP(dia, sfm[x])
    if(CL == 0):
      CL = getCL(dia, materal, endmilltype)
    ipr = CL * numOfTeeth
    ipm = ipr * rpm
    speeds.append({'num':x,'RPM':rpm, 'SFM':sfm[x] ,'IPR': ipr, 'IPM':ipm, "ChipLoad": CL})
  return speeds
  

print getSpeeds(0.5,4,materal="Aluminum 440, 356, 380, C61300",endmilltype="Carbide")


""" "":{
      SFM:"",
      "1/8":,
      "3/16":,
      "1/4":,
      "3/8":,
      "1/2":,
      "5/8":,
      "3/4":,
      "1":,
    }"""

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
