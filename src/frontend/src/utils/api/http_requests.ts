import config from "../config";

export async function post(route:string, body: object): Promise<any> {
    let response = await fetch(`${config.API_URL}${route}`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + localStorage.getItem("access_token"),
        },
        body: JSON.stringify(body),
    });
    if (!response.ok)
        throw "not ok"
    return await response.json();
}

export async function postFormData(route:string, body: FormData): Promise<any> {
    let response = await fetch(`${config.API_URL}${route}`, {
        method: "POST",
        body: body,
    });
    return await response.json();
}

export async function get(route:string, params: object = {}): Promise<any> {
    let encodedParams = [];
    for (let key in params) {
        encodedParams.push(`${key}=${params[key]}`)
    }
    let response = await fetch(`${config.API_URL}${route}?${encodedParams.join('&')}`, {
        method: 'GET',
        credentials: 'include',
        headers: {
            'Authorization': 'Bearer ' + localStorage.getItem("access_token"),
            'Content-Type': 'application/json'
        },
    });
    return await response.json();
}

export async function del(route:string, params: object = {}): Promise<any> {
    let encodedParams = [];
    for (let key in params) {
        encodedParams.push(`${key}=${params[key]}`)
    }
    let response = await fetch(`${config.API_URL}${route}?${encodedParams.join('&')}`,{
        method: "DELETE",
        credentials: 'include',
        headers: {
            'Authorization': 'Bearer ' + localStorage.getItem("access_token"),
            'Content-Type': 'application/json'
        },
    });
    return await response.json();
}