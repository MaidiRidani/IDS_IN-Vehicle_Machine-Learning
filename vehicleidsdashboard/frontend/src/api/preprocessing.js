const API_URL = "http://127.0.0.1:8000";

export async function getDatasets() {

    const response = await fetch(
        `${API_URL}/datasets`
    );

    if (!response.ok) {

        throw new Error(
            "Gagal mengambil dataset."
        );

    }

    return await response.json();

}


export async function loadDataset(datasetName) {

    const response = await fetch(

        `${API_URL}/dataset/load`,

        {

            method: "POST",

            headers: {

                "Content-Type": "application/json"

            },

            body: JSON.stringify({

                dataset_name: datasetName

            })

        }

    );

    if (!response.ok) {

        throw new Error(
            "Gagal memuat dataset."
        );

    }

    return await response.json();

}


export async function getLabels() {

    const response = await fetch(

        `${API_URL}/labels`

    );

    if (!response.ok) {

        throw new Error(
            "Gagal mengambil label."
        );

    }

    return await response.json();

}

export async function getModels() {

    const response = await fetch(

        `${API_URL}/models`

    );

    if (!response.ok) {

        throw new Error(
            "Gagal mengambil model."
        );

    }

    return await response.json();

}



export async function getPackets(

    label,

    offset = 0,

    limit = 500,

) {

    const response = await fetch(

        `${API_URL}/packets/${label}?offset=${offset}&limit=${limit}`

    );

    if (!response.ok) {

        throw new Error(
            "Gagal mengambil packet."
        );

    }

    return await response.json();

}

export async function addConfiguration(

    packetNumber,

    position,

) {

    const response = await fetch(

        `${API_URL}/configuration/add`,

        {

            method: "POST",

            headers: {

                "Content-Type": "application/json",

            },

            body: JSON.stringify({

                packet_number: packetNumber,

                position: position,

            }),

        }

    );

    if (!response.ok) {

        const error = await response.json();

        throw new Error(
            error.detail
        );

    }

    return await response.json();

}

export async function getWindowConfigurations() {

    const response = await fetch(

        `${API_URL}/window/configurations`

    );

    if (!response.ok) {

        throw new Error(
            "Gagal mengambil window configuration."
        );

    }

    return await response.json();

}

export async function getPreprocessingConfiguration() {

    const response = await fetch(

        `${API_URL}/configuration`

    );

    if (!response.ok) {

        throw new Error("Gagal mengambil preprocessing configuration.");

    }

    return await response.json();

}

export async function removeConfiguration(packetNumber) {

    const response = await fetch(

        `${API_URL}/configuration/${packetNumber}`,

        {

            method: "DELETE",

        }

    );

    if (!response.ok) {

        const error = await response.json();

        throw new Error(error.detail);

    }

    return await response.json();

}


export async function clearConfigurations() {

    const response = await fetch(

        `${API_URL}/configuration`,

        {

            method: "DELETE",

        }

    );

    if (!response.ok) {

        const error = await response.json();

        throw new Error(error.detail);

    }

    return await response.json();

}

export async function prepareWindows() {

    const response = await fetch(

        `${API_URL}/window/prepare`,

        {

            method: "POST",

        }

    );

    if (!response.ok) {

        const error = await response.json();

        throw new Error(error.detail);

    }

    return await response.json();

}

export async function getPreparedWindows() {

    const response = await fetch(

        `${API_URL}/window/prepared`

    );

    if (!response.ok) {

        const error = await response.json();

        throw new Error(error.detail);

    }

    return await response.json();

}

export async function runPreprocessing() {

    const response = await fetch(

        `${API_URL}/preprocessing/run`,

        {

            method: "POST",

        }

    );

    if (!response.ok) {

        const error = await response.json();

        throw new Error(error.detail);

    }

    return await response.json();

}

export async function getPreprocessedImages() {

    const response = await fetch(

        `${API_URL}/preprocessing/images`

    );

    if (!response.ok) {

        const error = await response.json();

        throw new Error(error.detail);

    }

    return await response.json();

}
export function getPreprocessedImageUrl(index) {

    return `${API_URL}/preprocessing/image/${index}`;

}

// =====================================================
// CONFIGURATION
// =====================================================

export async function saveConfiguration(

    windowSize,

    dwtLevel,

) {

    const response = await fetch(

        `${API_URL}/configuration`,

        {

            method: "POST",

            headers: {

                "Content-Type": "application/json",

            },

            body: JSON.stringify({

                window_size: windowSize,

                dwt_level: dwtLevel,

            }),

        }

    );

    if (!response.ok) {

        throw new Error(

            "Gagal menyimpan konfigurasi."

        );

    }

    return response.json();

}


export async function getConfiguration() {

    const response = await fetch(

        `${API_URL}/configuration`

    );

    if (!response.ok) {

        throw new Error(

            "Gagal mengambil konfigurasi."

        );

    }

    return response.json();

}


export async function generateRandomConfigurations(count) {

    const response = await fetch(

        `${API_URL}/configuration/random`,

        {

            method: "POST",

            headers: {

                "Content-Type": "application/json",

            },

            body: JSON.stringify({

                count,

            }),

        }

    );

    if (!response.ok) {

        throw new Error(

            "Gagal membuat konfigurasi random."

        );

    }

    return response.json();

}