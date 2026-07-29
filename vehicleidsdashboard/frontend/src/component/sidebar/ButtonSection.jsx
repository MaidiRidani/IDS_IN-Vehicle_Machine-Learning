import Panel from "../common/Panel";

function ButtonSection({

    setShowWindowBuilder,
    preprocessedImages,
    datasetLoaded,

    onRunDetection,

    onToggleLoop,

    loopRunning,

}) {
    const detectionReady =

        preprocessedImages.length > 0;
    console.log("preprocessedImages:", preprocessedImages.length);
    console.log("detectionReady:", detectionReady);
    return (
        <Panel
            border={false}
            className="
                relative
                w-[213px]
                h-[64px]
            "
        >

            {/* Choose Packet */}
            <button
                disabled={!datasetLoaded}

                style={{
                    backgroundColor: datasetLoaded
                        ? "#13832F"
                        : "#778795"
                }}

                onMouseEnter={(e) => {

                    if (datasetLoaded) {

                        e.currentTarget.style.backgroundColor = "#16A53C";

                    }

                }}

                onMouseLeave={(e) => {

                    if (datasetLoaded) {

                        e.currentTarget.style.backgroundColor = "#13832F";

                    }

                }}

                className={`
                    absolute
                    top-0
                    left-0
                    w-[213px]
                    h-[27px]
                    rounded-full
                    text-[12px]
                    font-bold
                    ${
                        datasetLoaded
                            ? "bg-[#13832F]"
                            : "bg-[#778795] cursor-not-allowed"
                    }
                `}
                onClick={() => {

                    if (datasetLoaded) {

                        setShowWindowBuilder(true);

                    }

                }}
            >
                CHOOSE PACKET
            </button>

            {/* Run Detection */}
            <button
                disabled={!detectionReady}
                onClick={onRunDetection}

                style={{
                    backgroundColor: detectionReady
                        ? "#13832F"
                        : "#778795"
                }}

                onMouseEnter={(e) => {

                    if (detectionReady) {

                        e.currentTarget.style.backgroundColor = "#16A53C";

                    }

                }}

                onMouseLeave={(e) => {

                    if (detectionReady) {

                        e.currentTarget.style.backgroundColor = "#13832F";

                    }

                }}
                className={`
                    absolute
                    top-[35px]
                    left-0
                    w-[213px]
                    h-[27px]
                    rounded-full
                    text-[12px]
                    font-bold
                    ${
                        detectionReady

                            ? "bg-[#13832F]"

                            : "bg-[#778795] cursor-not-allowed"}
                    `}
            >
                <img
                    src="/iconkecil/starticon.svg"
                    alt="Start"
                    className="
                        absolute
                        left-[29px]
                        top-[6px]
                    "
                />

                RUN DETECTION

            </button>

            <button
                disabled={!detectionReady}
                onClick={onToggleLoop}

                style={{
                    backgroundColor: !detectionReady
                        ? "#778795"
                        : loopRunning
                            ? "#B91C1C"
                            : "#0E7490",
                }}

                onMouseEnter={(e) => {

                    if (!detectionReady) return;

                    e.currentTarget.style.backgroundColor =
                        loopRunning
                            ? "#DC2626"
                            : "#0891B2";

                }}

                onMouseLeave={(e) => {

                    if (!detectionReady) return;

                    e.currentTarget.style.backgroundColor =
                        loopRunning
                            ? "#B91C1C"
                            : "#0E7490";

                }}

                className={`
                    absolute
                    top-[70px]
                    left-0
                    w-[213px]
                    h-[20px]
                    rounded-full
                    text-[12px]
                    font-bold
                    ${
                        detectionReady
                            ? ""
                            : "bg-[#778795] cursor-not-allowed"
                    }
                `}
            >
                {
                    loopRunning
                        ? "STOP LOOP"
                        : "RUN LOOP"
                }
            </button>

        </Panel>
    );
}

export default ButtonSection;