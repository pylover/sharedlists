
HOST="localhost:5555"
CURL="curl $HOST"
USER=
TOKEN=

function l.login() {
	USER=$1
	TOKEN=`$CURL -XLOGIN -F"email=$1" -F"password=$2" 2> /dev/null`
	if [ $? != 0 ]; then
		echo "Invalid email or password"
		return 1
	else
		echo "Welcome: $USER"
	fi
}


function _auth() {
	echo "Authorization: $TOKEN"
}


function l.list() {
	$CURL/$USER/$1 -H"$(_auth)"
}


function l.append() {
	$CURL/$USER/$1/$2 -H"$(_auth)" -XAPPEND
}

