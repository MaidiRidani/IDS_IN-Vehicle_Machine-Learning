import Panel from "../common/Panel";
import {
    getValidConfigurations,
} from "../../utils/dwtConfiguration";
import { useState, useMemo, useEffect } from "react";
import { saveConfiguration } from "../../api/preprocessing";




function ConfigureSection({

    loadedModel,

    selectedWindow,
    setSelectedWindow,

    selectedLevel,
    setSelectedLevel,
    hasConfiguration,
    setShowConfigurationLockedDialog,

}) {
    const [showWindowList, setShowWindowList] = useState(false);
    const validConfigurations = useMemo(() => {

        if (!loadedModel) {

            return [];

        }

        const inputSize = loadedModel.input_shape[1];

        return getValidConfigurations(inputSize);

    }, [loadedModel]);

    const availableWindows = [

        ...new Set(

            validConfigurations.map(

                config => config.windowSize

            )

        ),

    ];
    


    useEffect(() => {

        if (validConfigurations.length === 0) {

            return;

        }

        async function initializeConfiguration() {

            const config = validConfigurations[0];

            setSelectedWindow(

                config.windowSize

            );

            setSelectedLevel(

                config.level

            );

            await saveConfiguration(

                config.windowSize,

                config.level

            );

        }

        initializeConfiguration();

    }, [

        validConfigurations,

        setSelectedWindow,

        setSelectedLevel,

    ]);

    async function handleSelectWindow(windowSize) {

        setSelectedWindow(windowSize);

        const config = validConfigurations.find(
            item => item.windowSize === windowSize
        );

        if (config) {

            setSelectedLevel(config.level);

            try {

                await saveConfiguration(
                    windowSize,
                    config.level
                );

            } catch (error) {

                console.error(error);

            }

        }

        setShowWindowList(false);

    }

    return (
        <Panel
            className="
                relative
                w-[213px]
                h-[89px]
            "
        >

            {/* Title */}
            <h2
                className="
                    text-center
                    text-[12px]
                    font-bold
                    mt-[9px]
                "
            >
                KONFIGURASI
            </h2>

            <div
                className="absolute left-[6px]"
                style={{ top: "32px" }}
            >

                <div className="flex justify-between">

                    {/* Build Window */}
                    <div className="relative">

                        <p
                            className="
                                text-[10px]
                                font-normal
                                mb-[6px]
                            "
                        >
                            Build Window
                        </p>

                        <button

                            type="button"

                            className="
                                w-[100px]
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

                                setShowWindowList(

                                    prev => !prev

                                );

                            }}

                        >

                            <span className="text-[10px]">

                                {

                                    selectedWindow

                                        ? `${selectedWindow} × ${selectedWindow}`

                                        : "-"

                                }

                            </span>
                            <img
                                src="/iconkecil/dropdown.svg"
                                alt="Dropdown"
                                className="w-[12px] h-[12px]"
                            />

                        </button>

                        {

                            showWindowList && (

                                <div
                                    className="
                                        absolute
                                        top-[30px]
                                        left-0
                                        w-[100px]
                                        rounded-[10px]
                                        border
                                        border-white
                                        bg-[#17233A]
                                        overflow-hidden
                                        z-50
                                    "
                                >

                                    {

                                        availableWindows.map(

                                            windowSize => (

                                                <button

                                                    key={windowSize}

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
                                                        handleSelectWindow(
                                                            windowSize
                                                        )
                                                    }

                                                >

                                                    {windowSize} × {windowSize}

                                                </button>

                                            )

                                        )

                                    }

                                </div>

                            )

                        }

                    </div>

                    {/* Level DWT */}
                    <div>

                        <p
                            className="
                                text-[10px]
                                font-normal
                                mb-[6px]
                            "
                        >
                            Level DWT
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
                                justify-center
                            "
                        >

                            <span className="text-[10px]">
                                {
                                    selectedLevel

                                        ? `Level ${selectedLevel}`

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

export default ConfigureSection;