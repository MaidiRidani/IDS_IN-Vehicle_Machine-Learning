import Panel from "../common/Panel";
import { useEffect } from "react";
import { CLASS_INFO } from "../../constants/classInfo";

function ConfusionMatrixSection({

    history,

}) {


    useEffect(() => {

        console.log(

            "LIVE CONFUSION MATRIX",

            matrix

        );

    }, [history]);


    const labels = Object.keys(CLASS_INFO);
    const matrix = {};

    labels.forEach(gt => {

        matrix[gt] = {};

        labels.forEach(pred => {

            matrix[gt][pred] = {

                count: 0,

                windows: [],

            };

        });

    });
    console.log(history);
    (history ?? []).forEach(item => {

        const cell =

            matrix[item.groundTruth][item.prediction];

        cell.count++;

        cell.windows.push(item);

    });
    
    console.log("matrix",matrix)

    function buildTooltip(gt, pred) {

        const windows =

            matrix[gt][pred].windows;

        if (windows.length === 0) {

            return "";

        }

        return windows
            .slice(0, 5)
            .map(item =>

                `Packet : ${item.packet_number}
    Prediction : ${item.prediction}
    Confidence : ${item.confidence}%
    Time : ${item.timestamp}`

            )
            .join("\n\n");

    }


        
    return (
        <Panel
            className="
                relative
                w-[410px]
                h-[278px]
            "
        >

            {/* Title */}

            <h2
                className="
                    absolute
                    text-[16px]
                    font-bold
                "
                style={{
                    left: "20px",
                    top: "24px",
                }}
            >
                CONFUSION MATRIX
            </h2>

            {/* Matrix Area */}

            <div
                className="
                    absolute
                    w-[382px]
                    h-[205px]
                    rounded-[10px]
                    border
                    border-white
                    overflow-hidden
                    flex
                    items-center
                    justify-center
                "
                style={{
                    left: "14px",
                    top: "61px",
                }}
            >

                {/* Placeholder sementara */}

                <table className="w-full h-full text-[10px] text-center">

                    <thead>

                        <tr>

                            <th 
                                className="
                                    border
                                    border-[#334155]
                                    bg-[#17233A]
                                    text-[10px]
                                    font-bold
                                    w-[60px]
                                "
                            >
                                GT\Pred
                            </th>

                            {

                                labels.map(label => (

                                    <th
                                        key={label}
                                        className="
                                            border
                                            border-[#334155]
                                            bg-[#17233A]
                                            text-[10px]
                                            font-bold
                                            h-[28px]
                                            
                                        "
                                    >
                                        {label}
                                    </th>

                                ))

                            }

                        </tr>

                    </thead>

                    <tbody>

                        {

                            labels.map(gt => (

                                <tr key={gt}>

                                    <th
                                       className="border border-[#334155]"
                                    >
                                        {gt}
                                    </th>

                                    {

                                        labels.map(pred => (

                                            <td
                                                key={pred}
                                                title={buildTooltip(gt, pred)}
                                                className="
                                                    border
                                                    border-[#334155]
                                                    text-[10px]
                                                    font-bold
                                                    transition-colors
                                                "
                                                style={{

                                                    background:

                                                        gt === pred && matrix[gt][pred].count > 0

                                                            ? "#13832F"

                                                            : gt !== pred && matrix[gt][pred].count > 0

                                                                ? "#8B1E1E"

                                                                : "transparent",

                                                    color:

                                                        matrix[gt][pred].count === 0

                                                            ? "#64748B"

                                                            : "#FFFFFF",

                                                }}
                                            >

                                                {matrix[gt][pred].count}

                                            </td>

                                        ))

                                    }

                                </tr>

                            ))

                        }

                    </tbody>

                </table>

            </div>

        </Panel>
    );
}

export default ConfusionMatrixSection;