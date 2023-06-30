window.onload = async function() {
    console.log('ready -- initialize lights');
    toggleLoading(false)
    sendPost('init');

    let rand = Math.random() + 0.01
    let loadTime =  rand * 7000
    await setTimeout(() => {
        toggleLoading(true)
    }, loadTime)
};

function toggleLoading(hide) {
    document.getElementById('loadingScreen').hidden = hide;
}

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
        console.error(message);
    } else {
        console.log(message)
    }

}

