import json
import os
import shutil

def parse_configs():
    tools_dir = os.path.dirname(os.path.realpath(__file__))

    # load configs
    config_file = os.path.join(tools_dir, "release-configs.json")
    with open (config_file) as configs:
        data = json.load(configs)

    release_meta = data["release"]
    release_package_name = "apache-yunikorn-incubating-{0}-{1}".format(release_meta["version"],release_meta["release-candidate-version"])
    repo_list = data["repositories"]

    print("release meta info:")
    print(" - main version: %s" % release_meta["version"])
    print(" - release cadidate: %s" % release_meta["release-candidate-version"])
    print(" - release package name: %s" % release_package_name)

    staging_dir = os.path.join(os.path.dirname(tools_dir), "staging")
    release_base = os.path.join(staging_dir, release_package_name)
    release_top_path = os.path.join(os.path.dirname(tools_dir), "release-top-level-artifacts")

    # setup artifacts in the relase base dir
    setup_base_dir(release_top_path, release_base)

    for repo_meta in repo_list:
        setup_repo_artifacts(repo_meta)

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

def setup_repo_artifacts(repo_meta):
    print("setup...")
    print(repo_meta)


def main():
    parse_configs()

if __name__ == "__main__":
    main()
