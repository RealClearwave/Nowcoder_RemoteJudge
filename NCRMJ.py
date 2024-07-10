import requests,json
import sys

argv = sys.argv
if '-h' in argv or '--help' in argv or len(argv) == 1:
    print("Usage: NCRMJ.py [options] [file.cpp/file.py]")
    print("Options:")
    print("  -h, --help\t\tShow this help message and exit")
    print("  -l [language]\t\tSpecify the language of the code")
    print("  -p [problem]\t\tSpecify the problem name")
    print("  -s [contest_id] [username]\t\tShow the status of the user in the contest")
    print("Example:")
    print("  NCRMJ.py -l C++(clang++ 11.0.1) -p A A.cpp")
    exit()

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

if '-s' in argv:
    contest_id = argv[argv.index('-s')+1]
    user_name = argv[argv.index('-s')+2]
    r = requests.get(f"https://ac.nowcoder.com/acm-heavy/acm/contest/real-time-rank-data?token=&id={contest_id}&searchUserName={user_name}&limit=0",cookies=cookies)
    x = json.loads(r.text)
    x = x['data']['rankData'][0]
    print(f"\033[34mRank: {x['ranking']} Accepted: {x['acceptedCount']} Score:{x['totalScore']} Penalty: {x['penaltyTime']//1000}")
    print("Details:")

    scoreList = x['scoreList']

    for i in range(len(scoreList)):
        print(f"{"\033[92m" if scoreList[i]['accepted'] == True else "\033[91m"}",end="")
        print(f"Problem: {chr(65+i)} {"Accepted" if scoreList[i]['accepted'] == True else f'Unaccepted(-{scoreList[i]['failedCount']})'} Score: {scoreList[i]['score']}")
    
    print("\033[0m")
    exit()

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

res = submit_code(problemName,code,languageID,languageName)
resHundredRate = int(res["rightHundredRate"])
resDesc = res["desc"]
#print(resHundredRate,resDesc)
print("\033[34mScore: {}%: [".format(resHundredRate), "▋" * (resHundredRate // 2),' '* ((100-resHundredRate)//2),']')
print(f"{"\033[92m" if resHundredRate == 100 else "\033[91m"}Description: {resDesc}")
print("\033[0m")