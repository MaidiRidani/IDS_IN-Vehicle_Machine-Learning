import Header from "./Header";
import Sidebar from "./Sidebar";
import MainContent from "./MainContent";
import WindowBuilder from "./WindowBuilder";
import { useEffect, useState } from "react";
import ConfigurationLockedDialog
from "../common/ConfigurationLockedDialog";
import {

    clearConfigurations,

} from "../../api/preprocessing";


function DashboardLayout() {
    const [showWindowBuilder, setShowWindowBuilder] = useState(false);
    const [datasetLoaded, setDatasetLoaded] = useState(false);

    const [preprocessedImages, setPreprocessedImages] = useState([]);
    const [detectionResult, setDetectionResult] = useState(null);
    const [currentDetection, setCurrentDetection] = useState(null);
    const [detectionHistory, setDetectionHistory] = useState([]);
    const [selectedModel, setSelectedModel] = useState("");
    const [loadedModel, setLoadedModel] = useState(null);
    const [selectedWindow, setSelectedWindow] = useState(null);

    const [selectedLevel, setSelectedLevel] = useState(null);
    const [attackDistribution, setAttackDistribution] = useState({});
    const [hasConfiguration, setHasConfiguration] = useState(false);
    const [showConfigurationLockedDialog, setShowConfigurationLockedDialog] =
    useState(false);
    useEffect(() => {

        async function initialize() {

            try {

                await clearConfigurations();

            }

            catch (error) {

                console.error(error);

            }

        }

        initialize();

    }, []);


    useEffect(() => {

        if (!detectionResult) {

            return;

        }

        setDetectionHistory([]);

        let index = 0;

        const interval = setInterval(() => {

            const detection = detectionResult.results[index];
            const event = {

                timestamp: detection.timestamp,

                packet_number: detection.packet_number,

                prediction: detection.prediction,

                confidence: detection.confidence,

                average_latency_ms: detection.average_latency_ms,

                groundTruth: detection.window_label,

                correct: detection.is_correct,

            };

            setCurrentDetection(detection);

            setDetectionHistory(prev => [

                ...prev,

                event,

            ]);

            index++;

            if (index >= detectionResult.results.length) {

                clearInterval(interval);

            }

        }, 300);

        return () => clearInterval(interval);

    }, [detectionResult]);


    useEffect(() => {

        console.log(

            "History:",

            detectionHistory.length

        );

    }, [detectionHistory]);

    useEffect(() => {

        const distribution = {

            Normal: 0,

            F_I: 0,

            P_I: 0,

            M_F: 0,

            C_D: 0,

            C_R: 0,

        };

        detectionHistory.forEach(item => {

            distribution[item.prediction]++;

        });

        setAttackDistribution(distribution);

    }, [detectionHistory]);

    return (

        <div className="w-screen h-screen bg-[#08111F]">

            <div
                className="
                    relative
                    overflow-hidden
                    w-full
                    h-full
                    border
                    border-white
                "
            >
                            <Header

                    summary={detectionResult?.summary}

                    history={detectionHistory}

                />

                <div
                    className="
                        mt-0
                        grid
                        grid-cols-[233px_1fr]
                        gap-0
                    "
// CSS Grid menggunakan `align-items: stretch` secara default.
// Item yang lebih kecil akan di-stretch mengikuti tinggi baris grid.
// Jika suatu item memiliki tinggi lebih besar dari tinggi baris, maka tinggi baris akan mengikuti item tersebut.
// Karena Sidebar memiliki tinggi yang ditentukan sendiri, perilaku stretch lebih terlihat pada <main>.
                >
                    <Sidebar
                        setShowWindowBuilder={setShowWindowBuilder}
                        setDetectionResult={setDetectionResult}
                        selectedModel={selectedModel}
                        setSelectedModel={setSelectedModel}
                        preprocessedImages={preprocessedImages}
                        loadedModel={loadedModel}
                        setLoadedModel={setLoadedModel}

                        selectedWindow={selectedWindow}
                        setSelectedWindow={setSelectedWindow}

                        selectedLevel={selectedLevel}
                        setSelectedLevel={setSelectedLevel}

                        datasetLoaded={datasetLoaded}
                        setDatasetLoaded={setDatasetLoaded}
                        hasConfiguration={hasConfiguration}
                        setShowConfigurationLockedDialog={
                            setShowConfigurationLockedDialog
                        }

                    />
                    <MainContent 
                        preprocessedImages={preprocessedImages}
                        currentDetection={currentDetection}
                        detectionHistory={detectionHistory}
                        attackDistribution={attackDistribution}
                        detectionResult={detectionResult}
                    />

                </div>
                <WindowBuilder
                    show={showWindowBuilder}
                    setShow={setShowWindowBuilder}
                    loadedModel={loadedModel}
                    setPreprocessedImages={setPreprocessedImages}
                    selectedWindow={selectedWindow}
                    setHasConfiguration={setHasConfiguration}
                    selectedLevel={selectedLevel}
                />

                <ConfigurationLockedDialog

                    show={showConfigurationLockedDialog}

                    onClose={() =>

                        setShowConfigurationLockedDialog(false)

                    }

                />
            </div>

        </div>

    );

}

export default DashboardLayout;