import {del, get, post} from "./http_requests";
import type {FileDto} from "./api";

export async function saveTestbenchFiles(files: FileDto[], projectId: string): Promise<void> {
    await post("/save_testbench_files", {
        project_id: parseInt(projectId, 10),
        files: files.map(x => ({
            name: x.filename,
            code: x.content,
            metadata: ""
        })),
    });
}

export async function removeTestbenchFile(id: number) {
    await del("/delete_value/testbench_files", {
       id
    });
}

export async function getTestbenchFiles(projectId: number) {
    let files = await get("/get_files_to_student", { project_id: projectId });
    return files.map(x => ({
        filename: x.name,
        content: x.code,
        id: x.id,
    }));
}