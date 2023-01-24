import argparse
import json
import sys

parser = argparse.ArgumentParser()
parser.add_argument("--externalRelease", help ="Path of external release",required=True)
parser.add_argument("--platform", help ="Platform where qa will run",required=True)
parser.add_argument("--config_key", help ="Config key",required=True)
parser.add_argument("--build_type", help ="Build type",required=True)
args = parser.parse_args()

def getPlatforms(config_key,platform):
    platforms = ["linux_x86_64_rhel7","linux_x86_64_ubuntu20"]
    return platforms

qaDirs = {'central_default': {}}
qaDirs['central_default']['linux_x86_64_rhel7'] = {}
#qaDirs['central_default']['linux_x86_64_rhel7']["Optimized"] = ["short","medium","customer","linsol","scspice","cluster","pa_sc/medium","pfs_sc/medium","stable","seascape_training","sc_release","pfs_sc/customer","flow","rhsc_et/medium","ttsc/short","ttsc/medium", "rhsc_et/customer", "security_sc/short", "security_sc/short","security_sc/customer","short-db", "short-db-release", "medium-db","medium-db-release"]
qaDirs['central_default']['linux_x86_64_rhel7']["Optimized"] = ["short","medium"]
qaDirs['central_default']['linux_aarch64_ubuntu20'] = {}
qaDirs['central_default']['linux_aarch64_ubuntu20']["Optimized"] = qaDirs['central_default']['linux_x86_64_rhel7']["Optimized"]
qaDirs['central_default_with_debug_and_x86_ubuntu'] = {}
qaDirs['central_default_with_debug_and_x86_ubuntu']['linux_x86_64_rhel7'] = {}
qaDirs['central_default_with_debug_and_x86_ubuntu']['linux_x86_64_rhel7']["Optimized"] = ["short","medium","customer","linsol","scspice","cluster","pa_sc/medium","pfs_sc/medium","stable","seascape_training","sc_release","pfs_sc/customer","flow","rhsc_et/medium","ttsc/short","ttsc/medium", "rhsc_et/customer", "security_sc/short", "security_sc/short","security_sc/customer","short-db", "short-db-release", "medium-db","medium-db-release"]
#qaDirs['central_default_with_debug_and_x86_ubuntu']['linux_x86_64_rhel7']["Optimized"] = ["short","medium"]
qaDirs['central_default_with_debug_and_x86_ubuntu']['linux_x86_64_rhel7']["Debug"] = ["short"]
qaDirs['central_default_with_debug_and_x86_ubuntu']['linux_x86_64_ubuntu20'] = {}
qaDirs['central_default_with_debug_and_x86_ubuntu']['linux_x86_64_ubuntu20']["Optimized"] = ["short","medium"]

def createQAMatrix(central_db_dir,central_db_dir_relase,qaOpts):
    qaMatrix = {}
    qaMatrix['short'] = qaOpts  + "-j 12 --num_local_workers 1 --sc_behavior central --product redhawk_sc" 
    qaMatrix['medium'] = qaOpts  + "-j 12 --num_local_workers 1 --sc_behavior central --product redhawk_sc" 
    qaMatrix['customer'] = qaOpts  + "-j 12 --include_labels customer_default --product redhawk_sc" 
    qaMatrix['cluster'] = qaOpts  + "-j 12 --product redhawk_sc" 
    qaMatrix['stable'] = qaOpts  + "-j 12 --product redhawk_sc" 
    qaMatrix['linsol'] = qaOpts  + "-j 12" 
    qaMatrix['scspice'] = qaOpts  + "-j 12" 
    qaMatrix['pa_sc/medium'] = qaOpts  + "-j 10 --sc_behavior central --exclude_labels requires_pa_root --product powerartist_sc"
    qaMatrix['pfs_sc/medium'] = qaOpts  + "-j 6 --sc_behavior central --product pfs_sc"
    qaMatrix['seascape_training'] = qaOpts  + "-j 12 --product redhawk_sc" 
    qaMatrix['sc_release'] = qaOpts  + "-j 12 --product redhawk_sc" 
    qaMatrix['pfs_sc/customer'] = qaOpts  + "-j 7 --sc_behavior central --product pfs_sc"
    qaMatrix['flow'] = qaOpts  + "-j 12" 
    qaMatrix['rhsc_et/medium'] = qaOpts  + "-j 12 --sc_behavior central --product redhawk_sc"
    qaMatrix['ttsc/short'] = qaOpts  + "-j 6 --sc_behavior central"
    qaMatrix['ttsc/medium'] = qaOpts  + "-j 6 --sc_behavior central --product totem_sc"
    qaMatrix['rhsc_et/customer'] = qaOpts  + "-j 4 --sc_behavior central --product redhawk_sc"
    qaMatrix['security_sc/short'] = qaOpts  + "-j 12 --sc_behavior central"
    qaMatrix['security_sc/medium'] = qaOpts  + "-j 8 --sc_behavior central"
    qaMatrix['security_sc/customer'] = qaOpts  + "-j 9 --sc_behavior central --product security_sc"
    qaMatrix['short-db'] = qaOpts  + "-j 12 --check_db_compatibility --central_db_dir " + central_db_dir + "/short  --product redhawk_sc --log_file qa.db_compat_prev.log --status_json qa.db_compat_prev_status.json"
    qaMatrix['medium-db'] = qaOpts  + "-j 10 --check_db_compatibility --central_db_dir " + central_db_dir + "/medium  --product redhawk_sc --log_file qa.db_compat_prev.log --status_json qa.db_compat_prev_status.json"
    qaMatrix['short-db-release'] = qaOpts  + "-j 12 --check_db_compatibility --run_dir_tag release-22_R2 --central_db_dir " + central_db_dir_relase + "/short --product redhawk_sc --log_file qa.db_compat_release-22_R2.log --status_json qa.db_compat_release-22_R2_status.jsonn"
    qaMatrix['medium-db-release'] = qaOpts  + "-j 10 --check_db_compatibility --run_dir_tag release-22_R2 --central_db_dir " + central_db_dir_relase + "/medium --product redhawk_sc --log_file qa.db_compat_release-22_R2.log --status_json qa.db_compat_release-22_R2_status.json"
    return qaMatrix

platforms = getPlatforms(args.config_key,args.platform)
matrix = {}
matrix['include'] = []
for platform in platforms:
    if platform in qaDirs[args.config_key].keys():
        central_db_dir = "/projs00/scbuild/main/previous/" + args.platform + "/" + args.build_type + "/thk/dev/qa"
        central_db_dir_relase = "/projs00/scbuild/release-22_R2/latest/" + args.platform + "/" + args.build_type + "/thk/dev/qa"
        if args.build_type in ['Optimized']:
            qaOpts="--build " + args.build_type + " --force --report_time --external_release " + args.externalRelease + " "
        else:
            qaOpts="--build " + args.build_type + " --force --report_time "
        qaMatrix = createQAMatrix(central_db_dir,central_db_dir_relase,qaOpts)
        if args.build_type in qaDirs[args.config_key][platform]:
            for dir in qaDirs[args.config_key][platform][args.build_type]:
                tempDict = {"build_type": args.build_type, "platform": platform,"qa-dir": dir, "qa-opts" : qaMatrix[dir]}
                if dir in ('short-db', 'short-db-release'):
                    tempDict["qa-dir"] = "short"
                if dir in ('medium-db', 'medium-db-release'):
                    tempDict['qa-dir'] = "medium"
                matrix['include'].append(tempDict)

if not matrix['include']:
    sys.exit(43)
else:
    print(json.dumps(matrix))
