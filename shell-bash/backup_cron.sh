temp=$(mktemp -d)
cd $temp

git clone "git@github.com:carlosgit2016/backups.git"

cd backups

git config user.name "carlosgit2016" && git config user.email carlosggflor@gmail.com

crontab -l > crontab_user

git add .
msg="crontabbackup-$(date +%e/%m/%G\ %H:%M)"
git commit -m "$msg"
git branch -M main
git push -u origin main
