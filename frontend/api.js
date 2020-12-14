const _apiRequest = (route, method, payload) => {
    
    const options = {
        'method': method,
        'headers': {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }
    }

    if (method == 'POST' || method == 'UPDATE') {
        options['body'] = JSON.stringify(payload);
    }

    return fetch('http://127.0.0.1:5000' + route, options).then(
        response => response.json().then(data => data));
};

const apiPOST = (route, payload) => {
    return _apiRequest(route, 'POST', payload);
};

const apiUPDATE = (route, payload) => { 
    return _apiRequest(route, 'UPDATE', payload);
};

const apiGET = (route) => {
    return _apiRequest(route, 'GET', {});
};
