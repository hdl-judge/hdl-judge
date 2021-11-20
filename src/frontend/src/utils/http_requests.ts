import config from "./config";

export async function post(route:string, body: object): Promise<any> {
    let response = await fetch(`${config.API_URL}${route}`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(body)
    });
    return await response.json();
}

export async function get(route:string, params: object = {}): Promise<any> {
    let encodedParams = [];
    for (let key in params) {
        encodedParams.push(`${key}=${params[key]}`)
    }
    let response = await fetch(`${config.API_URL}${route}?${encodedParams.join('&')}`);
    return await response.json();
}

export async function del(route:string, params: object = {}): Promise<any> {
    let encodedParams = [];
    for (let key in params) {
        encodedParams.push(`${key}=${params[key]}`)
    }
    let response = await fetch(`${config.API_URL}${route}?${encodedParams.join('&')}`,{
        method: "DELETE"
    });
    return await response.json();
}