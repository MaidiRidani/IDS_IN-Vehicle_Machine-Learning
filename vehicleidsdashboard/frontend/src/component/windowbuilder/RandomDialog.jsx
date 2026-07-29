import Panel from "../common/Panel";

function RandomDialog({

    show,

    randomCount,

    setRandomCount,

    onCancel,

    onGenerate,

}) {

    if (!show) {

        return null;

    }

    return (

        <Panel
            className="
                absolute
                left-1/2
                top-1/2
                -translate-x-1/2
                -translate-y-1/2
                w-[320px]
                h-[180px]
                z-[100]
            "
            background="#0056A1"
        >

            <h2
                className="
                    text-center
                    text-[18px]
                    font-bold
                    mt-[16px]
                "
            >
                Random Configuration
            </h2>

            <p
                className="
                    text-center
                    text-[12px]
                    mt-[20px]
                "
            >
                Number of Configurations
            </p>

            <div className="flex justify-center mt-[10px]">

                <input

                    type="number"

                    min="1"

                    value={randomCount}

                    onChange={(e) =>
                        setRandomCount(
                            Number(e.target.value)
                        )
                    }

                    className="
                        w-[90px]
                        h-[32px]
                        rounded
                        text-center
                        text-black
                    "

                />

            </div>

            <div
                className="
                    flex
                    justify-center
                    gap-4
                    mt-[28px]
                "
            >

                <button

                    onClick={onCancel}

                    className="
                        px-4
                        py-2
                        rounded
                        bg-gray-500
                    "

                >
                    Cancel
                </button>

                <button

                    onClick={onGenerate}

                    className="
                        px-4
                        py-2
                        rounded
                        bg-green-600
                    "

                >
                    Generate
                </button>

            </div>

        </Panel>

    );

}

export default RandomDialog;