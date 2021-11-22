import {del, get, post} from "./http_requests";


export async function getAllUsers() {
    return await get("/get_values/users");
}

export async function addUser(name: string, email_address: string, academic_id: string, is_admin: boolean) {
    await post("/create_user", {
        name,
        email_address,
        academic_id,
        is_admin,
        is_professor: is_admin,
    });
}

export async function removeUser(id: number) {
    await del("/delete_value/users", {
       id
    });
}