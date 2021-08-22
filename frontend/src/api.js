import config from "./config"

async function executeTest(vhdFile) {
	const formData = new FormData();
	formData.append('file', vhdFile);

	let response = await fetch(`${config.API_URL}/test/execute`, {
		method: "POST",
		body: formData
	});

	return response.blob()
}

export {
	executeTest
}