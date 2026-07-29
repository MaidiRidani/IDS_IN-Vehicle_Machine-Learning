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
                h-[800px]
                flex-1
                p-[13px]
            "
        >

            <div
                className="
                    flex
                    gap-[7px]
                "
            >
                <DwtRgbSection
                    className="basis-[2%]"
                    preprocessedImages={preprocessedImages}
                />

                <DetectionTrendSection
                    className="flex-1"
                    history={detectionHistory}
                />
            </div>

            <div
                className="
                    flex
                    gap-[7px]
                    mt-[10px]
                "
            >

                <LiveDetectionSection
                    detection={currentDetection}
                />

                <RecentDetectionSection
                    history={detectionHistory}
                />

            </div>
            <div
                className="
                    flex
                    gap-[7px]
                    mt-[10px]
                "
            >

                <ConfusionMatrixSection
                    history={detectionHistory}
                />

                <CONFIDENCETREND
                    history={detectionHistory}
                />

                <AttackDistributionSection
                    distribution={attackDistribution}
                />

            </div>


        </Panel>
    );
}

export default MainContent;