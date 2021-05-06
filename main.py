import os,logging,toml,subprocess


def get_files(path):
    repo_list=[]
    for filepath,dirnames,filenames in os.walk(path):
        for filename in filenames:
            repo_list.append(os.path.join(filepath,filename))
    return repo_list

def sync(list):
    for i in range(len(list)):
        dict = toml.load(list[i])
        GITHUB_TOKEN = dict.get("github_token")
        UPSTREAM_REPO = dict.get("upstream_repository")
        TARGET_REPO = dict.get("target_repository")
        UPSTREAM_BRANCH = dict.get("target_branch", "master")
        TARGET_BRANCH = dict.get("target_branch", "master")
        FORCE = dict.get("force", False)
        TAG = dict.get("tags", False)
        _FORCE = ""
        _TAG = ""
        _GITHUB_TOKEN = None

        if GITHUB_TOKEN == None:
            _GITHUB_TOKEN = os.environ.get("FORK_TOKEN", None)
            if _GITHUB_TOKEN == None:
                logger.warning("%s : 未获取到TOKEN,跳过", list[i])
                continue
        else:
            _GITHUB_TOKEN = os.environ.get(GITHUB_TOKEN, None)
            if _GITHUB_TOKEN == None:
                logger.warning("%s : 未获取到TOKEN,跳过", list[i])
                continue

        if UPSTREAM_REPO == None:
            logger.warning("%s : 未获取到远程仓库,跳过", list[i])
            continue

        if TARGET_REPO == None:
            logger.warning("%s : 未获取到推送仓库,跳过", list[i])
            continue

        if FORCE == True:
            _FORCE = "--force"

        if TAG == True:
            _TAG = "--tags"

        upstream_repo = "https://" + os.environ.get(GITHUB_ACTOR) + ":" + _GITHUB_TOKEN + "@github.com/" + UPSTREAM_REPO + ".git"
        upstream_dir = "${" + UPSTREAM_REPO + "##*/}"
        target_repo = "https://" + os.environ.get(GITHUB_ACTOR) + ":" + _GITHUB_TOKEN + "@github.com/" + TARGET_REPO + ".git"
        
        setup_one = "git clone " + upstream_repo
        setup_two = "cd " + upstream_dir
        setup_three = "git push " + _FORCE + " --follow-tags" + _TAG + target_repo + UPSTREAM_BRANCH + ":" + TARGET_BRANCH
        subprocess.call(setup_one)
        subprocess.call(setup_two)
        subprocess.call(setup_three)



def main():

    #当前路径
    path_work = os.path.dirname(os.path.realpath(__file__))
    logger.info("脚本运行目录: %s", path_work)

    #仓库同步路径
    path_sync = path_work+"/sync_repo/"
    logger.info("仓库订阅目录: %s", path_sync)
    repo_list = get_files(path_sync)
    sync(repo_list)

if __name__ == '__main__':
    logging.basicConfig(level = logging.INFO,format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logger = logging.getLogger(__name__)
    main()



