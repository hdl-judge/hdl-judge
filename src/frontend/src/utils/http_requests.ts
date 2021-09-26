import config from "./config";

export function post(route:string, body: object): Promise<Response> {
    return fetch(`${config.API_URL}${route}`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(body)
    });
}