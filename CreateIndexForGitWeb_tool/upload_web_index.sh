# This shell is used to automatically upload index_for_web.json to io repo

# --- Command line
src_file=$1
commit_msg=$2

# set basic variables
cur_dir=$3
owner="ibmpredictiveanalytics"
repo_name="IBMPredictiveAnalytics.github.io"
file_name="index_for_web.json"
sub_folder="resbundles"
abs_repo_folder=$cur_dir/$repo_name

# --- Permission check
chmod u+w "$cur_dir"
if [ ! -w "$cur_dir" ]; then
	echo "Need write permission in $cur_dir!" >&2
	exit 1
fi

if [ ! -f "$src_file" ]; then
	echo "$src_file does not exist!" >&2
	exit 1
fi

if [ -d "$abs_repo_folder" ]; then
	echo "$abs_repo_folder already exists! Delete it?(y/n):"
	read user_cmd
	if [ "$user_cmd"="y" ] || [ "$user_cmd"="Y" ]; then
		if [ -x "$abs_repo_folder" ]; then
			rm -rf "$abs_repo_folder"
		else
			echo "Need permission to delete $abs_repo_folder" >&2
		fi
	else
		exit 1
	fi
fi

# clone repo from github
cd $cur_dir
git clone git@github.com:$owner/$repo_name.git

# get tar file path
tar_file="$cur_dir/$repo_name/$sub_folder/$file_name"
chmod u+w "$tar_file"
if [ ! -w "$tar_file" ]; then
	echo "Need write permission in $tar_file!" >&2
	exit 1
fi

cp -f "$src_file" "$tar_file"
cd "$cur_dir/$repo_name"
git commit -am "$commit_msg"
git push origin master
