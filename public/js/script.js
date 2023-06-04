window.onload = function() {
    console.log('ready -- initialize lights')
};

function sendPost(message) {
    req = {'behaviour':message};

    fetch('http://192.168.2.28:8081/changeLight', {
        method: 'POST',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(req)
    })
    .then((response) => {
        response.json().then((message) => {
            handlePostResult(message)
        });
    });
}

function handlePostResult(message) {
    if(message.startsWith('Error')) {
        alert(message);
    } else {
        console.log(message)
    }

}

