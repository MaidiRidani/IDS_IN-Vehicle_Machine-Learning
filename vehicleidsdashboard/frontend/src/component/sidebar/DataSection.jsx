import { useEffect, useState } from "react";
import Panel from "../common/Panel";

import {
    getDatasets,
    loadDataset,
} from "../../api/preprocessing";
function DataSection({

    setDatasetLoaded,

}) {

    const [datasets, setDatasets] = useState([]);

    const [selectedDataset, setSelectedDataset] = useState("");
    const [showDatasetList, setShowDatasetList] = useState(false);

    const [datasetInfo, setDatasetInfo] = useState(null);
    useEffect(() => {

        async function initialize() {

            try {

                const data = await getDatasets();

                setDatasets(data);

                if (data.length > 0) {

                    const info = await loadDataset(
                        data[0].id
                    );

                    setSelectedDataset(
                        data[0].id
                    );

                    setDatasetInfo(
                        info
                    );

                    // Beritahu parent bahwa dataset sudah siap
                    setDatasetLoaded(true);

                }

            }

            catch (error) {

                setDatasetLoaded(false);
                console.error(error);

            }

        }

        initialize();

    }, []);
    async function handleSelectDataset(datasetId) {

        try {

            const info = await loadDataset(
                datasetId
            );

            setSelectedDataset(
                datasetId
            );

            setDatasetInfo(
                info
            );

            setDatasetLoaded(true);

            setShowDatasetList(false);

        }

        catch (error) {

            setDatasetLoaded(false);
            console.error(error);

        }

    }
    return (
        <Panel
            className="
                relative
                w-[213px]
                h-[312px]
            "
        >

            {/* Refresh Dataset */}
            <button
                className="
                    absolute
                    top-[8px]
                    right-[8px]
                    w-[16px]
                    h-[16px]
                    flex
                    items-center
                    justify-center
                    cursor-pointer
                "
                onClick={() => {

                    if (selectedDataset) {

                        handleSelectDataset(
                            selectedDataset
                        );

                    }

                }}
            >
                <img
                    src="/iconkecil/refresh.svg"
                    alt="Refresh"
                    className="w-full h-full object-contain"
                />
            </button>

            <h2
                className="
                    text-center
                    text-[12px]
                    font-bold
                    mt-[10px]
                "
            >
                PILIH DATA
            </h2>

            {/* Dataset */}
            <div
                className="absolute left-[6px]"
                style={{ top: "35px" }}
            >

                <p
                    className="
                        text-[10px]
                        font-normal
                        mb-[6px]
                    "
                >
                    Dataset
                </p>

                <div
                    className="
                        relative
                        w-[200px]
                    "
                >

                    <button
                        type="button"
                        className="
                            w-[200px]
                            h-[26px]
                            rounded-full
                            border
                            border-white
                            flex
                            items-center
                            justify-between
                            px-[10px]
                        "
                        onClick={() =>
                            setShowDatasetList(prev => !prev)
                        }
                    >

                        <span
                            className="
                                text-[10px]
                                font-normal
                            "
                        >
                            {
                                datasets.find(
                                    d => d.id === selectedDataset
                                )?.name ?? "-"
                            }
                        </span>

                        <img
                            src="/iconkecil/dropdown.svg"
                            alt="Dropdown"
                            className="
                                w-[12px]
                                h-[12px]
                                object-contain
                            "
                        />

                    </button>

                    {
                        showDatasetList && (

                            <div
                                className="
                                    absolute
                                    top-[30px]
                                    left-0
                                    w-[200px]
                                    rounded-[10px]
                                    border
                                    border-white
                                    bg-[#17233A]
                                    overflow-hidden
                                    z-50
                                "
                            >

                                {
                                    datasets.map(dataset => (

                                        <button
                                            key={dataset.id}
                                            type="button"
                                            className="
                                                w-full
                                                px-[10px]
                                                py-[6px]
                                                text-left
                                                text-[10px]
                                                hover:bg-[#2A4E7A]
                                            "
                                            onClick={() =>
                                                handleSelectDataset(dataset.id)
                                            }
                                        >

                                            {dataset.name}

                                        </button>

                                    ))
                                }

                            </div>

                        )
                    }

                </div>

            </div>

            {/* Label Dataset */}
            <div
                className="absolute left-[6px]"
                style={{ top: "86px" }}
            >

                <p
                    className="
                        text-[10px]
                        font-normal
                        mb-[6px]
                    "
                >
                    Label Dataset
                </p>

                <div
                    className="
                        w-[200px]
                        h-[26px]
                        rounded-full
                        border
                        border-white
                        flex
                        items-center
                        px-[10px]
                    "
                >

                    <span
                        className="
                            text-[10px]
                            font-normal
                        "
                    >
                        Loaded
                    </span>
                </div>

            </div>

            {/* Packet Information */}
            <div
                className="absolute left-[6px]"
                style={{ top: "145px" }}
            >

                <div className="flex justify-between">

                    {/* Total Packet */}
                    <div>

                        <p
                            className="
                                text-[10px]
                                font-normal
                                mb-[6px]
                            "
                        >
                            Total Packet
                        </p>

                        <div
                            className="
                                w-[100px]
                                h-[26px]
                                rounded-full
                                border
                                border-white
                                flex
                                items-center
                                px-[10px]
                            "
                        >
                            <span className="text-[10px]">
                                {
                                    datasetInfo?.total_packets ?? "-"
                                }
                            </span>
                        </div>

                    </div>

                    {/* Captured */}
                    <div>

                        <p
                            className="
                                text-[10px]
                                font-normal
                                mb-[6px]
                            "
                        >
                            Captured
                        </p>

                        <div
                            className="
                                w-[100px]
                                h-[26px]
                                rounded-full
                                border
                                border-white
                                flex
                                items-center
                                px-[10px]
                            "
                        >
                            <span className="text-[10px]">
                                24 Mei 2025
                            </span>
                        </div>

                    </div>

                </div>

            </div>


            {/* Jenis-jenis Label */}
            <div
                className="absolute left-[6px]"
                style={{ top: "199px" }}
            >

                <p
                    className="
                        text-[10px]
                        font-normal
                        mb-[6px]
                    "
                >
                    Jenis-jenis Label
                </p>

                <div
                    className="
                        w-[200px]
                        h-[80px]
                        rounded-[10px]
                        border
                        border-white
                        p-[6px]
                    "
                >

                    <div className="flex flex-wrap gap-[6px]">

                        {(datasetInfo?.labels ?? []).map((label) => (

                            <div
                                key={label}
                                className="
                                    w-[53px]
                                    h-[15px]
                                    rounded-[4px]
                                    border
                                    border-white
                                    flex
                                    items-center
                                    justify-center
                                    text-[8px]
                                    font-normal
                                "
                            >
                                {label}
                            </div>

                        ))}

                    </div>

                </div>

            </div>

        </Panel>
    );
}

export default DataSection;