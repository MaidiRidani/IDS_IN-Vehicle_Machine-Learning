export async function getModels() {

    const response = await fetch(

        "http://127.0.0.1:8001/models"

    );

    if (!response.ok) {

        throw new Error(
            "Gagal mengambil model."
        );

    }

    return await response.json();

}


export async function loadModel(modelName) {

    const response = await fetch(

        "http://127.0.0.1:8001/model/load",

        {

            method: "POST",

            headers: {

                "Content-Type": "application/json"

            },

            body: JSON.stringify({

                model_name: modelName

            })

        }

    );

    if (!response.ok) {

        throw new Error(
            "Gagal memuat model."
        );

    }

    return await response.json();

}


export async function getCurrentModel() {

    const response = await fetch(

        "http://127.0.0.1:8001/model/current"

    );

    if (!response.ok) {

        throw new Error(

            "Gagal mengambil model aktif."

        );

    }

    return await response.json();

}



export async function runDetection() {

    const response = await fetch(

        "http://127.0.0.1:8001/detection/run",

        {

            method: "POST",

        }

    );

    if (!response.ok) {

        throw new Error(

            "Gagal menjalankan deteksi."

        );

    }

    return await response.json();

}



