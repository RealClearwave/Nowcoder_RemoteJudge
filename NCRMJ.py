import requests,json
import sys

lang_map = {
    "C++(clang++ 11.0.1)":2,
    "Python3":11
}

with open("cookie.txt","r") as f:
    cookie_str = f.read()

cookies = dict(item.split('=') for item in cookie_str.split('; '))

with open("problemset.json","r") as f:
    problems = json.load(f)

def submit_code(problemName, code, languageID, languageName):
    url = 'https://ac.nowcoder.com/nccommon/submit_cd?'
    data = {
        'questionId': problems[problemName]["questionId"],
        'tagId': problems[problemName]["tagId"],
        'subTagId': problems[problemName]["subTagId"],
        'content': code,
        'language': languageID,
        'languageName': languageName,
        'doneQuestionId': problems[problemName]["doneQuestionId"],
    }
    r =requests.post(url,data,cookies=cookies)

    print(r.text)
    x = json.loads(r.text)
    print(f"RID: {x['data']}")

    print("Waiting for judge...")
    while True:
        url = f"https://ac.nowcoder.com/nccommon/status?submissionId={x['data']}&tagId={data['tagId']}&subTagId={data['subTagId']}"
        r = requests.get(url,cookies=cookies)
        #print(r.text)
        xx = json.loads(r.text)
        if not "等待判题" in xx["desc"]:
            break

    return json.loads(r.text)


#print(submit_code("B",code_A,2,"C++(clang++ 11.0.1)"))

argv = sys.argv

if '-h' in argv or '--help' in argv or not '.cpp' in ' '.join(argv) and not '.py' in ' '.join(argv):
    print("NCRMJ.py - NowCoder RemoteJudge by Clearwave")
    print("Usage: NCRMJ.py [code] [-l language] [-p problem]")
    print("Example: NCRMJ.py A.cpp -l C++ -p A")
    sys.exit()

for arg in argv:
    if '.cpp' in arg or '.py' in arg:
        codeName = arg
        if '.cpp' in arg:
            languageName = "C++(clang++ 11.0.1)"
            languageID = lang_map["C++(clang++ 11.0.1)"]
            problemName = arg.replace(".cpp","")
        elif '.py' in arg:
            languageName = "Python3"
            languageID = lang_map["Python3"]
            problemName = arg.replace(".py","")

        print(f"Code: {arg}")
        with open(arg,"r",encoding='utf-8') as f:
            code = f.read()

if '-l' in argv:
    languageName = argv[argv.index('-l')+1]
    if languageName.lower() == "c++":
        languageName = "C++(clang++ 11.0.1)"
    languageID = lang_map[languageName]

if '-p' in argv:
    problemName = argv[argv.index('-p')+1]

print(f"Problem: {problemName}")
print(f"Language: {languageName}")

print(submit_code(problemName,code,languageID,languageName))