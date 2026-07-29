import Panel from "../common/Panel";
import { useEffect, useState } from "react";
import { CLASS_INFO } from "../../constants/classInfo";
import {
    PieChart,
    Pie,
    Cell,
    ResponsiveContainer,
    Tooltip,
} from "recharts";



function AttackDistributionSection({

    distribution,

    className = "",

}) {

    const classes = Object.entries(CLASS_INFO);

    const chartData = classes

        .map(([key, info]) => ({

            name: info.displayName,

            value: distribution?.[key] ?? 0,

            color: info.color,

        }))

        .filter(item => item.value > 0);

    useEffect(() => {

        console.log("DISTRIBUSI DI SECTION",distribution);

    }, [distribution]);
    const totalWindows = chartData.reduce(

        (sum, item) => sum + item.value,

        0

    );

    function CustomTooltip({

        active,

        payload,

    }) {

        if (!active || !payload?.length) {

            return null;

        }

        const item = payload[0].payload;

        return (

            <div
                className="
                    rounded-[8px]
                    border
                    border-white
                    bg-[#101B30]
                    px-[10px]
                    py-[6px]
                "
            >

                <p
                    className="text-[11px] font-bold"
                    style={{
                        color: item.color,
                    }}
                >
                    {item.name}
                </p>

                <p className="text-[10px]">

                    Count : {item.value}

                </p>

            </div>

        );

    }
    return (

        <Panel
            className={`
                relative
                h-[278px]
                flex-1
                min-w-0
                ${className}
            `}
        >
                    {/* ================= Title ================= */}

            <h2
                className="
                    absolute
                    text-[16px]
                    font-bold
                "
                style={{
                    left: "10px",
                    top: "20px",
                }}
            >
                ATTACK DISTRIBUTION
            </h2>

            {/* ================= Chart Placeholder ================= */}
            {/* ================= Chart ================= */}

            <div
                className="
                    absolute
                    rounded-[10px]
                    border
                    border-white
                "
                style={{
                    left: "8px",
                    right: "145px",
                    top: "61px",
                    bottom: "18px",
                }}
            >

                <ResponsiveContainer
                    width="100%"
                    height="100%"
                >

                    <PieChart>
                        <Tooltip content={<CustomTooltip />} />
                        <Pie
                            data={chartData}
                            dataKey="value"
                            cx="50%"
                            cy="50%"
                            innerRadius={48}
                            outerRadius={92}
                            paddingAngle={2}
                            stroke="none"
                            isAnimationActive={false}
                            animationDuration={300}
                            animationEasing="ease-out"
                        >

                            {
                                chartData.map((entry, index) => (

                                    <Cell
                                        key={index}
                                        fill={entry.color}
                                    />

                                ))
                            }

                        </Pie>

                    </PieChart>

                </ResponsiveContainer>
                <div
                    className="
                        absolute
                        inset-0
                        flex
                        flex-col
                        items-center
                        justify-center
                        pointer-events-none
                    "
                >

                    <span
                        className="
                            text-[22px]
                            font-bold
                        "
                    >
                        {totalWindows}
                    </span>

                    <span
                        className="
                            text-[10px]
                        "
                    >
                        WINDOWS
                    </span>

                </div>

            </div>

            {
                classes.map(

                    ([key, info], index) => (

                        <div
                            key={key}
                            className="absolute"
                            style={{

                                right:"115px",

                                top:`${40 + index*40}px`,

                            }}
                        >

                            <div
                                className="rounded-full"
                                style={{
                                    width: "15px",
                                    height: "15px",
                                    background: info.color,
                                }}
                            />

                            <span
                                className="
                                    absolute
                                    text-[9px]
                                    font-normal
                                    leading-[15px]
                                    break-words
                                "
                                style={{
                                    left: "21px",
                                    top: "0px",
                                    width:"65px",
                                }}
                            >
                                {info.displayName}
                            </span>

                            <span
                                className="
                                    absolute
                                    text-[10px]
                                    font-bold
                                "
                                style={{
                                    left:"70px",
                                    top: "2px",
                                    width: "25px",
                                    textAlign: "right",
                                }}
                            >
                                {distribution?.[key] ?? 0}
                            </span>

                        </div>

                    )

                )
            }

        </Panel>

    );

}

export default AttackDistributionSection;