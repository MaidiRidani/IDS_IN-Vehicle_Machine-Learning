import { useEffect, useState } from "react";
import Panel from "../common/Panel";


function ModelSection({

    models,

    loadedModel,

    selectedModel,

    setSelectedModel,

    onSelectModel,
    hasConfiguration,
    setShowConfigurationLockedDialog,

}) {


    const [showModelList, setShowModelList] = useState(false);

    function handleSelectModel(modelName) {

        if (hasConfiguration) {

            return;

        }

        setSelectedModel(modelName);

        onSelectModel(modelName);

        setShowModelList(false);

    }

    return (
        <Panel
            className="
                relative
                w-[213px]
                h-[201px]
            "
        >

            {/* Refresh */}
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
            >
                <img
                    src="/iconkecil/refresh.svg"
                    alt="Refresh"
                    className="w-full h-full object-contain"
                />
            </button>

            {/* Title */}
            <h2
                className="
                    text-center
                    text-[12px]
                    font-bold
                    mt-[10px]
                "
            >
                PILIH MODEL
            </h2>

            {/* Model */}
            <div
                className="absolute left-[6px]"
                style={{ top: "30px" }}
            >

                <p
                    className="
                        text-[10px]
                        font-normal
                        mb-[6px]
                    "
                >
                    Model
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
                        onClick={() => {

                            if (hasConfiguration) {
                                    setShowConfigurationLockedDialog(true);
                                
                                return;

                            }

                            setShowModelList(prev => !prev);

                        }}
                    >

                        <span className="text-[10px] font-normal">
                            {selectedModel ?? "-"}
                        </span>

                        <img
                            src="/iconkecil/dropdown.svg"
                            alt="Dropdown"
                            className="w-[12px] h-[12px]"
                        />

                    </button>

                    {

                        showModelList && (

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

                                   models.map(modelName => (

                                        <button

                                            key={modelName}

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
                                                handleSelectModel(modelName)
                                            }

                                        >

                                            {modelName}

                                        </button>

                                    ))

                                }

                            </div>

                        )

                    }

                </div>

            </div>

            {/* Framework & Classes */}
            <div
                className="absolute left-[6px]"
                style={{ top: "86px" }}
            >

                <div className="flex justify-between">

                    {/* Framework */}
                    <div>

                        <p
                            className="
                                text-[10px]
                                font-normal
                                mb-[6px]
                            "
                        >
                            Framework
                        </p>

                        <div
                            className="
                                w-[132px]
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
                                {loadedModel?.framework ?? "-"}
                            </span>

                        </div>

                    </div>

                    {/* Classes */}
                    <div>

                        <p
                            className="
                                text-[10px]
                                font-normal
                                mb-[6px]
                            "
                        >
                            Classes
                        </p>

                        <div
                            className="
                                w-[63px]
                                h-[26px]
                                rounded-full
                                border
                                border-white
                                flex
                                items-center
                                justify-center
                            "
                        >

                            <span className="text-[10px]">
                                {loadedModel?.output_classes ?? "-"}
                            </span>

                        </div>

                    </div>

                </div>

            </div>

            {/* Input Size & Model Size */}
            <div
                className="absolute left-[6px]"
                style={{ top: "141px" }}
            >

                <div className="flex justify-between">

                    {/* Input Size */}
                    <div>

                        <p
                            className="
                                text-[10px]
                                font-normal
                                mb-[6px]
                            "
                        >
                            Input Size
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
                                    loadedModel
                                        ? `${loadedModel.input_shape[1]} × ${loadedModel.input_shape[2]} × ${loadedModel.input_shape[3]}`
                                        : "-"
                                }

                            </span>

                        </div>

                    </div>

                    {/* Model Size */}
                    <div>

                        <p
                            className="
                                text-[10px]
                                font-normal
                                mb-[6px]
                            "
                        >
                            Model Size
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
                                    loadedModel
                                        ? `${loadedModel.file_size_mb} MB`
                                        : "-"
                                }

                            </span>

                        </div>

                    </div>

                </div>

            </div>

        </Panel>
    );
}

export default ModelSection;