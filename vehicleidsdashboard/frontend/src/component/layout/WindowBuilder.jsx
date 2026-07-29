import Panel from "../common/Panel";
import SelectTypePacketSection from "../windowbuilder/SelectTypePacketSection";
import ActionButtonSection from "../windowbuilder/ActionButtonSection";
import SummarySection from "../windowbuilder/SummarySection";
import AvailablePacketSection from "../windowbuilder/AvailablePacketSection";
import PacketConfigurationSection from "../windowbuilder/PacketConfigurationSection";
import ClearConfirmationDialog from "../windowbuilder/ClearConfirmationDialog";
import SuccessDialog from "../windowbuilder/SuccessDialog";
import { useEffect, useState } from "react";
import ErrorDialog from "../windowbuilder/ErrorDialog";
import {
    getLabels,
    getPackets,
    addConfiguration,
    getWindowConfigurations,
    removeConfiguration,
    clearConfigurations,
    prepareWindows,
    getPreparedWindows,
    runPreprocessing,
    getPreprocessedImages,
    saveConfiguration,
    generateRandomConfigurations,
} from "../../api/preprocessing";
import RandomDialog from "../windowbuilder/RandomDialog";


function WindowBuilder({

    show,
    loadedModel,
    setShow,
    selectedLevel,
    setPreprocessedImages,
    selectedWindow,
    setHasConfiguration,

}) {

    const DEFAULT_PACKET = 1023;
    const DEFAULT_POSITION = 122;
    const [selectedAttack, setSelectedAttack] = useState("");
    const [packetPage, setPacketPage] = useState(0);
    const [labels, setLabels] = useState([]);
    const [preparedWindows, setPreparedWindows] = useState([]);
    const [packets, setPackets] = useState([]);
    const [selectedPacket, setSelectedPacket] = useState(1023);
    const [windowPosition, setWindowPosition] = useState(122);
    const [configurations, setConfigurations] = useState([]);
    const [editingPacket, setEditingPacket] = useState(null);
    const [showClearDialog, setShowClearDialog] = useState(false);
    const [showErrorDialog, setShowErrorDialog] = useState(false);
    const [errorMessage, setErrorMessage] = useState("");
    const [showSuccessDialog, setShowSuccessDialog] = useState(false);
    const [successMessage, setSuccessMessage] = useState("");
    const hasConfiguration = configurations.length > 0;
    const [showRandomDialog, setShowRandomDialog] = useState(false);
    const [randomCount, setRandomCount] = useState("20");


    useEffect(() => {

        async function initialize() {

            try {

                const data = await getLabels();

                setLabels(data);

                if (data.length > 0) {

                    setSelectedAttack(data[0]);

                }
                await refreshConfigurations();

            }

            catch ( error) {

                console.error(error);

            }

        }

        initialize();

    }, []);
    useEffect(() => {

        setHasConfiguration(

            configurations.length > 0

        );

    }, [

        configurations,

        setHasConfiguration,

    ]);

    useEffect(() => {

        async function loadPackets() {

            if (!selectedAttack) {

                return;

            }

            try {

                const data = await getPackets(

                    selectedAttack,

                    packetPage * 500,

                    500,

                );

                setPackets(data);

            }

            catch (error) {

                console.error(error);

            }

        }

        loadPackets();

    }, [selectedAttack, packetPage]);


    function handleSelectAttack(label) {

        setSelectedAttack(label);

        setPacketPage(0);

    }
    function handleOpenClearDialog() {

        setShowClearDialog(true);

    }

    async function refreshConfigurations() {

        try {

            const data = await getWindowConfigurations();

            setConfigurations(data);

        }

        catch (error) {

            console.error(error);

        }

    }


    async function handleAddConfiguration() {

        try {

            await addConfiguration(

                selectedPacket,

                windowPosition,

            );

            await refreshConfigurations();

        }

        catch (error) {

            console.error(error);

            setErrorMessage(error.message);

            setShowErrorDialog(true);

        }

    }
    
    function handleSelectConfiguration(configuration) {

        setSelectedAttack(
            configuration.attack_type
        );

        setSelectedPacket(
            configuration.packet_number
        );

        setWindowPosition(
            configuration.position
        );

        setEditingPacket(
            configuration.packet_number
        );

    }
    function increaseWindowPosition() {

        setWindowPosition(prev =>

            prev < selectedWindow

                ? prev + 1

                : prev

        );

    }

    function handleSelectPacket(packetNumber) {

        setSelectedPacket(packetNumber);

        const configuration = configurations.find(
            config => config.packet_number === packetNumber
        );

        if (configuration) {

            handleSelectConfiguration(configuration);

        } else {

            setEditingPacket(null);

        }

    }

    function decreaseWindowPosition() {

        setWindowPosition(prev =>

            prev > 1

                ? prev - 1

                : prev

        );

    }
    async function handleDeleteConfiguration(packetNumber) {

        try {

            await removeConfiguration(
                packetNumber
            );

            await refreshConfigurations();

            if (editingPacket === packetNumber) {

                setEditingPacket(null);

            }

        }

        catch (error) {

            console.error(error);

            setErrorMessage(error.message);

            setShowErrorDialog(true);

        }

    }

    async function handleSave() {

        try {

            const preparedResult = await prepareWindows();

            const preprocessingResult = await runPreprocessing();

            const images = await getPreprocessedImages();

            console.log(images);

            setPreprocessedImages(images);

            const prepared = await getPreparedWindows();

            console.log(prepared);

            setPreparedWindows(prepared);

            setSuccessMessage(

                `${preparedResult.prepared} windows prepared.\n` +
                `${preprocessingResult.processed} RGB images generated.`

            );

            setShowSuccessDialog(true);

        }

        catch (error) {

            console.error(error);

            setErrorMessage(error.message);

            setShowErrorDialog(true);

        }

    }
    async function handleClearConfigurations() {

        try {

            await clearConfigurations();

            await refreshConfigurations();

            setEditingPacket(null);

            if (labels.length > 0) {

                setSelectedAttack(labels[0]);

            }

            setSelectedPacket(DEFAULT_PACKET);

            setWindowPosition(DEFAULT_POSITION);


        }

        catch (error) {

            console.error(error);

            setErrorMessage(error.message);

            setShowErrorDialog(true);

        }

    }

    async function handleGenerateRandom() {

        try {

            await generateRandomConfigurations(

                randomCount

            );

            await refreshConfigurations();

            setShowRandomDialog(false);

        }

        catch (error) {

            console.error(error);

            setErrorMessage(error.message);

            setShowErrorDialog(true);

        }

    }

    const canSave =

        loadedModel !== null &&

        configurations.length > 0;


    return (

        <Panel
            className={`
                absolute
                left-0
                bottom-0
                w-[594px]
                h-[756px]
                z-50
                transition-transform
                duration-300
                ${show ? "translate-x-0" : "-translate-x-full"}
            `}
            background="#0056A1"
        >
            <div className="relative w-full h-full">

                {/* Title */}
                <h1
                    className="
                        absolute
                        text-[24px]
                        font-bold
                    "
                    style={{
                        left: "17px",
                        top: "13px",
                    }}
                >
                    WINDOW BUILDER
                </h1>
                {/* ================= Action Button ================= */}

                <ActionButtonSection
                    setShow={setShow}
                    canSave={canSave}
                    onSave={handleSave}
                    onClearConfigurations={handleOpenClearDialog}
                    onRandom={() =>
                        setShowRandomDialog(true)
                    }
                />

                {/* ================= Select Type Packet ================= */}

                <div
                    className="absolute"
                    style={{
                        left: "0px",
                        top: "60px",
                    }}
                >
                    <SelectTypePacketSection
                        labels={labels}
                        selectedAttack={selectedAttack}
                        setSelectedAttack={handleSelectAttack}
                    />
                </div>

                {/* ================= Summary ================= */}

                <div
                    className="absolute"
                    style={{
                        left: "225px",
                        top: "60px",
                    }}
                >

                    <SummarySection
                        configurations={configurations}
                        editingPacket={editingPacket}
                        onSelectConfiguration={handleSelectConfiguration}
                        onDeleteConfiguration={handleDeleteConfiguration}
                    />

                </div>

                {/* ================= Available Packet ================= */}

                <div
                    className="absolute"
                    style={{
                        left: "0px",
                        bottom: "2px",
                    }}
                >
                    <AvailablePacketSection
                        packets={packets}
                        packetPage={packetPage}
                        setPacketPage={setPacketPage}
                        selectedPacket={selectedPacket}
                        setSelectedPacket={handleSelectPacket}
                        configurations={configurations}
                    />
                </div>

                {/* ================= Packet Configuration ================= */}

                <div
                    className="absolute"
                    style={{
                        left: "302px",
                        bottom: "2px",
                    }}
                >

                    <PacketConfigurationSection
                        selectedAttack={selectedAttack}
                        selectedPacket={selectedPacket}
                        windowPosition={windowPosition}
                        setWindowPosition={setWindowPosition}
                        increaseWindowPosition={increaseWindowPosition}
                        decreaseWindowPosition={decreaseWindowPosition}
                        onAddConfiguration={handleAddConfiguration}
                        selectedWindow={selectedWindow}
                    />

                </div>

                {/* ================= Overlay ================= */}

                {
                    (showClearDialog || showErrorDialog || showSuccessDialog || showRandomDialog) && (
                        <div
                            className="
                                absolute
                                inset-0
                                bg-black/50
                                z-[90]
                            "
                        />
                    )
                }

                {/* ================= Clear Dialog ================= */}

                <ClearConfirmationDialog
                    show={showClearDialog}
                    onCancel={() => setShowClearDialog(false)}
                    onConfirm={async () => {

                        await handleClearConfigurations();

                        setShowClearDialog(false);

                    }}
                />

                <ErrorDialog
                    show={showErrorDialog}
                    message={errorMessage}
                    onClose={() => setShowErrorDialog(false)}
                />
                            </div>
                <SuccessDialog
                    show={showSuccessDialog}
                    message={successMessage}
                    onClose={() => {

                        setShowSuccessDialog(false);

                        setShow(false);

                    }}
                />

                <RandomDialog

                    show={showRandomDialog}

                    randomCount={randomCount}

                    setRandomCount={setRandomCount}

                    onCancel={() =>

                        setShowRandomDialog(false)

                    }

                    onGenerate={handleGenerateRandom}

                />
        </Panel>

    );
}

export default WindowBuilder;