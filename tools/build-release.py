import json
import os
import shutil
import git

def build_release():
    tools_dir = os.path.dirname(os.path.realpath(__file__))

    # load configs
    config_file = os.path.join(tools_dir, "release-configs.json")
    with open (config_file) as configs:
        data = json.load(configs)

    release_meta = data["release"]
    release_package_name = "apache-yunikorn-incubating-{0}-{1}".format(
        release_meta["version"],release_meta["release-candidate-version"])
    repo_list = data["repositories"]

    print("release meta info:")
    print(" - main version: %s" % release_meta["version"])
    print(" - release cadidate: %s" % release_meta["release-candidate-version"])
    print(" - release package name: %s" % release_package_name)

    staging_dir = os.path.join(os.path.dirname(tools_dir), "staging")
    release_base = os.path.join(staging_dir, release_package_name)
    release_top_path = os.path.join(os.path.dirname(tools_dir),
        "release-top-level-artifacts")

    # setup artifacts in the relase base dir
    setup_base_dir(release_top_path, release_base)

    for repo_meta in repo_list:
        dowload_sourcecode(release_base, repo_meta)

    # download helm chart templates
    print("creating helm chart templates")
    charts_src = os.path.join(release_base, "k8shim", "helm-charts")
    charts_dest = os.path.join(release_base, "helm-charts")
    shutil.copytree(charts_src, charts_dest)

def setup_base_dir(release_top_path, base_path):
    print("setting up base dir for release artifacts, path: %s" % base_path)
    if os.path.exists(base_path):
      raise Exception("staging dir %s already exist, please remove it and retry" % base_path)

    # setup base dir
    os.makedirs(base_path)
    # copy top level artifacts
    for file in os.listdir(release_top_path):
        org = os.path.join(release_top_path, file)
        dest = os.path.join(base_path, file)
        print("copying files: %s ===> %s" % (org, dest))
        shutil.copyfile(org, dest)

def dowload_sourcecode(base_path, repo_meta):
    print("downloading source code")
    print("repository info:")
    print(" - repository: %s " % repo_meta["repository"])
    print(" - description: %s " % repo_meta["description"])
    print(" - branch: %s " % repo_meta["branch"])
    print(" - hash: %s " % repo_meta["hash"])
    repo = git.Repo.clone_from(
        url=repo_meta["repository"],
        to_path=os.path.join(base_path, repo_meta["alias"]),
        b=repo_meta["branch"])
    repo.git.checkout(repo_meta["hash"])

def main():
    build_release()

if __name__ == "__main__":
    main()
