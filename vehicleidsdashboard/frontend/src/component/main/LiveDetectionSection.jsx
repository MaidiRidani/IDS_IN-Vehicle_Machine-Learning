import Panel from "../common/Panel";
import ProbabilityBar from "../main/ProbabilityBar";
import { useEffect } from "react";
import { CLASS_INFO } from "../../constants/classInfo";

function LiveDetectionSection({

    detection,

    className = "",

}) {
    useEffect(() => {

        console.log("result di live detectionsection",detection);

    }, [detection]);

    const prediction = detection?.prediction ?? "-";

    const predictionInfo = CLASS_INFO[prediction];

    const confidence = detection?.confidence ?? 0;

    const probabilities = detection?.probabilities ?? {};

    const probabilityList = Object.entries(probabilities)

        .sort((a, b) => b[1] - a[1])

        .slice(0, 6);
    
    return (
        <Panel
            className={`
                relative
                h-[182px]
                flex-1
                min-w-0
                ${className}
            `}
        >
            {/* Live Icon */}
            <img
                src="/sectionlivedetector/liveicon.svg"
                alt="Live"
                className="absolute"
                style={{
                    left: "36px",
                    top: "20px",
                }}
            />

            {/* Model Icon */}
            <img
                src="/sectionlivedetector/modelicon.svg"
                alt="Model"
                className="absolute"
                style={{
                    left: "233px",
                    top: "8px",
                }}
            />

            {/* Title Live Detection */}
            <h2
                className="
                    absolute
                    text-[16px]
                    font-bold
                "
                style={{
                    left: "62px",
                    top: "20px",
                }}
            >
                LIVE DETECTION
            </h2>

            {/* Title Top-6 */}
            <h2
                className="
                    absolute
                    text-[16px]
                    font-bold
                "
                style={{
                    left: "411px",
                    top: "20px",
                }}
            >
                TOP-6 PROBABILITAS
            </h2>

            {/* Prediction Box */}
            <div
                className="
                    absolute
                    w-[163px]
                    h-[58px]
                    rounded-[10px]
                    border
                    border-white
                    flex
                    flex-col
                    items-center
                "
                style={{
                    left: "36px",
                    top: "49px",
                }}
            >
                <p
                    className="
                        mt-[10px]
                        text-[10px]
                        font-normal
                        text-center
                    "
                >
                    PREDICTION
                </p>

                {/* Nantinya terhubung dengan Python */}
                <p
                    className="
                        mt-[3px]
                        text-[14px]
                        font-bold   
                        text-center
                    "
                    style={{
                        color: predictionInfo?.color ?? "#FFFFFF",
                    }}
                >
                    {predictionInfo?.displayName ?? "-"}
                </p>
            </div>
            {/* Confidence Box */}

            <div
                className="
                    absolute
                    w-[163px]
                    h-[58px]
                    rounded-[10px]
                    border
                    border-white
                "
                style={{
                    left: "36px",
                    top: "112px",
                }}
            >

                <p
                    className="
                        absolute
                        text-[10px]
                        font-normal
                    "
                    style={{
                        left: "49px",
                        top: "10px",
                    }}
                >
                    CONFIDENCE
                </p>

                {/* Nantinya terhubung dengan Python */}
                <p
                    className="
                        absolute
                        text-[16px]
                        font-bold
                    "
                    style={{
                        left: "52px",
                        top: "29px",
                        color: predictionInfo?.color ?? "#FFFFFF",
                    }}
                >
                    {confidence.toFixed(2)}%
                </p>

            </div>
            {
                probabilityList.map(

                    ([label, value], index) => (

                        <ProbabilityBar

                            key={label}

                            label={label}

                            value={value}

                            top={`${59 + index * 20}px`}

                        />

                    )

                )
            }

        </Panel>
    );
}

export default LiveDetectionSection;