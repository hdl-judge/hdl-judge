import {del, get, post} from "./http_requests";
import type {FileDto} from "./api";

export async function saveTestbenchFiles(files: FileDto[], projectId: string): Promise<void> {
    await post("/save_testbench_file", {
        project_id: parseInt(projectId, 10),
        file: {
            name: files[0].filename,
            code: files[0].content,
        },
    });
}

export async function removeTestbenchFile(id: number) {
    await del("/delete_value/testbench_files", {
       id
    });
}

export async function getTestbenchFiles(projectId: number) {
    let files = await get("/get_testbench_files", { project_id: projectId });
    if (!files || files.length < 1)
        return [{ filename: "testbench.vhdl", content: "", id: 0}]
    return files.map(x => ({
        filename: x.name,
        content: x.code,
        id: x.id,
    }));
}