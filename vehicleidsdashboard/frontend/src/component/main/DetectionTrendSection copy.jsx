import Panel from "../common/Panel";
import { useEffect } from "react";
import { CLASS_INFO } from "../../constants/classInfo";
import {

    ResponsiveContainer,

    LineChart,

    Line,

    XAxis,

    YAxis,

    CartesianGrid,

    Tooltip,

} from "recharts";




function DetectionTrendSection({

    history,

}) {


    const counts = {

        Normal: 0,

        F_I: 0,

        P_I: 0,

        M_F: 0,

        C_D: 0,

        C_R: 0,

    };

    const chartData = history.map(

        (item, index) => {

            counts[item.prediction]++;

            return {

                window: index + 1,

                ...counts,

            };

        }

    );

    useEffect(() => {

        console.log("CHARDATA",chartData);

    }, [chartData]);

    const classes = Object.entries(CLASS_INFO);

    function CustomTooltip({

        active,

        payload,

        label,

    }) {

        if (!active || !payload?.length) {

            return null;

        }

        return (

            <div
                className="
                    rounded-[8px]
                    border
                    border-white
                    bg-[#101B30]
                    px-[10px]
                    py-[8px]
                "
            >

                <p
                    className="
                        text-[11px]
                        font-bold
                        mb-[6px]
                    "
                >
                    WINDOW {label}
                </p>

                {

                    payload.map(item => (

                        <div
                            key={item.dataKey}
                            className="
                                flex
                                justify-between
                                gap-[15px]
                                text-[10px]
                            "
                        >

                            <span
                                style={{
                                    color: item.color,
                                }}
                            >
                                {CLASS_INFO[item.dataKey].displayName}
                            </span>

                            <span>

                                {item.value}

                            </span>

                        </div>

                    ))

                }

            </div>

        );

    }    


    return (
        <Panel
            className="
                relative
                w-[717px]
                h-[277px]
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
                    left: "9px",
                    top: "23px",
                }}
            >
                DETECTION TREND
            </h2>

            {/* Last 60 Minutes */}
            <span
                className="
                    absolute
                    text-[10px]
                    font-normal
                    text-[#2B9BFF]
                "
                style={{
                    left: "164px",
                    top: "32px",
                }}
            >
                (LAST 60 MINUTES)
            </span>

            {/* Chart Area */}
            <div
                className="
                    absolute
                    w-[638px]
                    h-[177px]
                    rounded-[10px]
                    border
                    border-white
                "
                style={{
                    left: "35px",
                    top: "53px",
                }}
            >
            <ResponsiveContainer
                width="100%"
                height="100%"
            >

                <LineChart
                    data={chartData}
                    margin={{
                        top: 10,
                        right: 20,
                        left: -15,
                        bottom: 5,
                    }}
                >

                    <CartesianGrid
                        stroke="#2E3D57"
                        strokeDasharray="2 2"
                    />

                    <XAxis
                        dataKey="window"
                        tick={{
                            fill: "#FFFFFF",
                            fontSize: 10,
                        }}
                        tickLine={false}
                        axisLine={{
                            stroke: "#FFFFFF",
                        }}
                        interval="preserveStartEnd"
                    />

                    <YAxis
                        allowDecimals={false}
                        domain={[0, "dataMax + 1"]}
                        tick={{
                            fill: "#FFFFFF",
                            fontSize: 10,
                        }}
                        tickLine={false}
                        axisLine={{
                            stroke: "#FFFFFF",
                        }}
                    />
                    <Tooltip

                        content={<CustomTooltip />}

                    />

                    {
                        classes.map(

                            ([key, info]) => (

                                <Line

                                    key={key}

                                    type="monotone"

                                    dataKey={key}

                                    stroke={info.color}

                                    strokeWidth={2}

                                    dot={false}

                                />

                            )

                        )
                    }

                </LineChart>

            </ResponsiveContainer>

            </div>

            {/* Legend */}
            <div
                className="
                    absolute
                    flex
                    items-center
                "
                style={{
                    left: "23px",
                    top: "252px",
                }}
            >
                {
                    classes.map(

                        ([key, info]) => (

                            <div
                                key={key}
                                className="flex items-center ml-[12px]"
                            >

                                <span
                                    className="text-[10px] font-normal"
                                >
                                    {info.displayName}
                                </span>

                                <div
                                    className="ml-[5px]"
                                    style={{
                                        width: "25px",
                                        height: "5px",
                                        background: info.color,
                                    }}
                                />

                            </div>

                        )

                    )
                }
            </div>

        </Panel>
    );
}

export default DetectionTrendSection;