import Panel from "../common/Panel";
import DataSection from "../sidebar/DataSection";
import ModelSection from "../sidebar/ModelSection";
import ConfigureSection from "../sidebar/ConfigureSection";
import ButtonSection from "../sidebar/ButtonSection";
import { useEffect, useState } from "react";
import {
    getModels,
    loadModel,
    getCurrentModel,
    runDetection,
} from "../../api/detection";

function Sidebar({

    setShowWindowBuilder,
    preprocessedImages,
    selectedModel,
    setSelectedModel,
    setDetectionResult,
    loadedModel,
    setLoadedModel,

    selectedWindow,
    setSelectedWindow,

    selectedLevel,
    setSelectedLevel,

    datasetLoaded,
    setDatasetLoaded,
    hasConfiguration,
    setShowConfigurationLockedDialog,

    loopRunning,
    onToggleLoop,
})
{

    const [models, setModels] = useState([]);

    useEffect(() => {

        async function initialize() {

            const data = await getModels();

            setModels(data);

        }

        initialize();

    }, []);

    async function handleSelectModel(modelName) {

        try {

            // update dropdown
            setSelectedModel(modelName);

            // load model ke backend
            const info = await loadModel(modelName);

            // update informasi model
            setLoadedModel(info);

        }

        catch (error) {

            console.error(error);

        }

    }

    async function handleRunDetection() {

        if (!datasetLoaded) {

            return;

        }

        if (!loadedModel) {

            return;

        }

        if (!hasConfiguration) {

            return;

        }

        try {

            const response = await runDetection();

            console.log("ini detection run button",response);

            setDetectionResult(response);

            console.log(response);

        }

        catch (error) {

            console.error(error);

        }

    }

    return (
        <Panel className="h-[800px] w-[233px]">



            {/* Sidebar Title */}
            <h1
                className="
                    ml-[12px]
                    mt-[12px]
                    text-[16px]
                    font-bold
                "
            >
                DETECTION CONTROL
            </h1>

            {/* Section 1 */}
            <div className="mt-[12px] flex justify-center"
            >
            

                <DataSection
                    setDatasetLoaded={setDatasetLoaded}
                />

            </div>

            <div className="mt-[8px] flex justify-center"
            >

                <ModelSection
                    models={models}
                    loadedModel={loadedModel}
                    onSelectModel={handleSelectModel}
                    selectedModel={selectedModel}
                    setSelectedModel={setSelectedModel}
                    hasConfiguration={hasConfiguration}
                    setShowConfigurationLockedDialog={
                        setShowConfigurationLockedDialog
                    }
                />

            </div>

            <div className="mt-[8px] flex justify-center">
                <ConfigureSection

                    loadedModel={loadedModel}

                    selectedWindow={selectedWindow}
                    setSelectedWindow={setSelectedWindow}

                    selectedLevel={selectedLevel}
                    setSelectedLevel={setSelectedLevel}
                    hasConfiguration={hasConfiguration}
                    setShowConfigurationLockedDialog={
                        setShowConfigurationLockedDialog
                    }

                />

            </div>

            {/* Button Section */}
            <div className="mt-[8px] flex justify-center">
                <ButtonSection
                    setShowWindowBuilder={setShowWindowBuilder}

                    datasetLoaded={datasetLoaded}

                    onRunDetection={handleRunDetection}

                    preprocessedImages={preprocessedImages}

                    loopRunning={loopRunning}

                    onToggleLoop={onToggleLoop}
                />

            </div>



        </Panel>
    );
}

export default Sidebar;