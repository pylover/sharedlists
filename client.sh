
SL_HOST="http://localhost:5555"
SL_USER=
SL_TOKEN=


function l.login() {
	SL_USER=$1
	SL_TOKEN=`curl $SL_HOST -XLOGIN -F"email=$1" -F"password=$2" 2> /dev/null`
	if [ $? != 0 ]; then
		echo "Invalid email or password"
		return 1
	else
		echo "Welcome: $SL_USER"
	fi
}

function curl_() {
	 curl --header "Authorization: ${SL_TOKEN}" --request $1 --url $SL_HOST/$2
}

function l.list() {
	if [ -z $1 ]; then
		user=$SL_USER
	else
		user=$1
	fi
	curl_ GET $user
}


function l.append() {
	curl_ APPEND $1
}


function l.delete() {
	curl_ DELETE $1
}
