const _apiRequest = (route, method, payload) => {
    
    const options = {
        'method': method,
        'headers': {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }
    }

    if (method == 'POST') {
        options['body'] = JSON.stringify(payload);
    }

    return fetch('http://127.0.0.1:5000' + route, options).then(
        response => response.json().then(data => data));
};

const apiPOST = (route, payload) => {
    return _apiRequest(route, 'POST', payload);
};

const apiGET = (route) => {
    return _apiRequest(route, 'GET', {});
};
