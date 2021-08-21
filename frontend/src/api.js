import config from "./config"

async function executeTest(vhdFile) {
	const formData = new FormData();
	formData.append('dataFile', vhdFile);

	let response = await fetch(`${config.API_URL}/test/execute`, {
		method: "POST",
		body: formData
	});

	return response.json()
}

export {
	executeTest
}