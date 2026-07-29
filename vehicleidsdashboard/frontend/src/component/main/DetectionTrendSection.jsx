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
    className = "",

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
            className={`
                relative
                flex-1
                h-[277px]
                ${className}
            `}
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
            <span className="text-[10px] text-[#2B9BFF]">   
                (LAST 60 MINUTES)
            </span>

            {/* Chart Area */}
            <div
                className="
                    absolute
                    h-[177px]
                    rounded-[10px]
                    border
                    border-white
                "
                style={{
                    left: 35,
                    right: 20,
                    top: 53,
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
                    left-[20px]
                    right-[20px]
                    bottom-[8px]
                    flex
                    flex-wrap
                    items-center
                    gap-x-[12px]
                    gap-y-[4px]
                "
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