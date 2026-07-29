import Panel from "../common/Panel";
import { useEffect } from "react";

function PacketConfigurationSection({
    selectedAttack,
    selectedPacket,
    windowPosition,
    setWindowPosition,
    increaseWindowPosition,
    decreaseWindowPosition,
    onAddConfiguration, 
    selectedWindow,
}) {
    useEffect(() => {

        if (!selectedWindow) return;

        if (windowPosition > selectedWindow) {

            setWindowPosition(selectedWindow);

        }

    }, [

        selectedWindow,

        windowPosition,

        setWindowPosition,

    ]);


    // console.log(selectedAttack);
    // console.log(selectedPacket);
    // console.log(windowPosition);
    console.log("🪟 Selected Window:", selectedWindow);
    return (

        <Panel
            className="
                relative
                w-[280px]
                h-[345px]
            "
        >

            {/* ================= Title ================= */}

            <h2
                className="
                    absolute
                    text-[16px]
                    font-bold
                "
                style={{
                    left: "13px",
                    top: "11px",
                }}
            >
                PACKET CONFIGURATION
            </h2>

            {/* ================= Type ================= */}

            <div
                className="
                    absolute
                    w-[249px]
                    h-[64px]
                    rounded-[10px]
                    border
                    border-white
                "
                style={{
                    left: "11px",
                    top: "43px",
                }}
            >

                <span
                    className="
                        absolute
                        text-[13px]
                        font-normal
                    "
                    style={{
                        left: "7px",
                        top: "4px",
                    }}
                >
                    Type
                </span>

                <span
                    className="
                        absolute
                        left-0
                        w-full
                        text-center
                        text-[16px]
                        font-bold
                        whitespace-nowrap
                    "
                    style={{
                        top: "20px",
                    }}
                >
                    {selectedAttack}
                </span>

            </div>

            {/* ================= Packet Number ================= */}

            <div
                className="
                    absolute
                    w-[249px]
                    h-[64px]
                    rounded-[10px]
                    border
                    border-white
                "
                style={{
                    left: "11px",
                    top: "116px",
                }}
            >

                <span
                    className="
                        absolute
                        text-[13px]
                        font-bold
                    "
                    style={{
                        left: "7px",
                        top: "5px",
                    }}
                >
                    Packet Number
                </span>

                <span
                    className="
                        absolute
                        text-[20px]
                        font-bold
                    "
                    style={{
                        left: "100px",
                        top: "30px",
                    }}
                >
                    {selectedPacket}
                </span>

            </div>

            {/* ================= Window Position ================= */}

            <span
                className="
                    absolute
                    text-[13px]
                    font-bold
                "
                style={{
                    left: "18px",
                    top: "199px",
                }}
            >
                Window Position
            </span>

            <div
                className="
                    absolute
                    w-[249px]
                    h-[50px]
                    rounded-[10px]
                    border
                    border-white
                "
                style={{
                    left: "11px",
                    top: "220px",
                }}
            >

                {/* Minus */}

                <button
                    className="
                        absolute
                        text-[20px]
                        font-bold
                    "
                    style={{
                        left: "10px",
                        top: "-2px",
                    }}
                    onClick={decreaseWindowPosition}
                >
                    −
                </button>

                {/* Slider */}

                <div
                    className="absolute"
                    style={{
                        left: "38px",
                        right: "38px",
                        top: "8px",
                    }}
                >

                    <input
                        type="range"
                        min="1"
                        max={selectedWindow || 0}
                        value={windowPosition}
                        onChange={(e) =>
                            setWindowPosition(Number(e.target.value))
                        }
                        className="w-full"
                    />

                    <div
                        className="
                            text-center
                            text-[12px]
                            font-bold
                            mt-[-2px]
                        "
                    >
                        {windowPosition}
                    </div>

                </div>

                {/* Plus */}

                <button
                    className="
                        absolute
                        text-[20px]
                        font-bold
                    "
                    style={{
                        right: "10px",
                        top: "-2px",
                    }}
                    onClick={increaseWindowPosition}
                >
                    +
                </button>

            </div>


            {/* ================= ADD CONFIGURATION ================= */}

            <button
                className="
                    absolute
                    w-[213px]
                    h-[27px]
                    rounded-full
                    bg-[#13832F]
                    text-[12px]
                    font-bold
                "
                style={{
                    left: "26px",
                    top: "295px",
                }}
                onClick={onAddConfiguration}
            >
                ADD Configuration
            </button>

        </Panel>

    );

}

export default PacketConfigurationSection;