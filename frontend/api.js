const apiPOST = (route, payload) => {
    return fetch('http://127.0.0.1:5000' + route, {
        'method': 'POST',
        'headers': {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        'body': JSON.stringify(payload)
    }).then(response => response.json().then(data => data));
};
