import Panel from "../common/Panel";
import DwtRgbSection from "../main/DwtRgbSection";
import DetectionTrendSection from "../main/DetectionTrendSection";
import LiveDetectionSection from "../main/LiveDetectionSection";
import RecentDetectionSection from "../main/RecentDetectionSection";
import ConfusionMatrixSection from "../main/ConfusionMatrixSection";
import CONFIDENCETREND from "../main/CONFIDENCETREND";
import { useEffect } from "react";
import AttackDistributionSection from "../main/AttackDistributionSection";



function MainContent({

    preprocessedImages,
    currentDetection,
    detectionHistory,
    attackDistribution,
    detectionResult,

}) {
    return (
        <Panel
            className="
                relative
                h-[765px]
                w-[1200px]
            "
        >

            <div
                className="absolute"
                style={{
                    left: "13px",
                    top: "0px",
                }}
            >
                <DwtRgbSection 
                    preprocessedImages={preprocessedImages}
                />
            </div>

            {/* DETECTION TREND */}
            <div
                className="absolute"
                style={{
                    left: "459px", // 13 + 439 + 7
                    top: "0px",
                }}
            >
                <DetectionTrendSection 
                    history={detectionHistory}
                />
            </div>

            <div
                className="absolute"
                style={{
                    left: "13px",
                    top: "287px",
                }}
            >
                <LiveDetectionSection
                    detection={currentDetection}
                />
            </div>

            <div
                className="absolute"
                style={{
                    left: "700px",
                    top: "287px",
                }}
            >
                <RecentDetectionSection 
                    history={detectionHistory}
                />
            </div>
            <div
                className="absolute"
                style={{
                    left: "9px",
                    top: "478px",
                }}
            >
                <ConfusionMatrixSection
                    history={detectionHistory}

                />
            </div>

            <div
                className="absolute"
                style={{
                    left: "424px",
                    top: "478px",
                }}
            >
                <CONFIDENCETREND 
                    history={detectionHistory}
                />
            </div>

            <div
                className="absolute"
                style={{
                    left: "851px",
                    top: "478px",
                }}
            >
                <AttackDistributionSection 
                    distribution={attackDistribution}
                />
            </div>


        </Panel>
    );
}

export default MainContent;