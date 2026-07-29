import Panel from "../common/Panel";

function ClearConfirmationDialog({
    show,
    onCancel,
    onConfirm,
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
                h-[170px]
                z-[100]
            "
            background="#0056A1"
        >

            <h2
                className="
                    text-center
                    text-[18px]
                    font-bold
                    mt-4
                "
            >
                CLEAR CONFIGURATION
            </h2>
            <p
                className="
                    text-center
                    text-[13px]
                    mt-[20px]
                    px-[20px]
                "
            >
                Are you sure you want to clear all configurations?
            </p>

            <div
                className="
                    absolute
                    bottom-[18px]
                    left-0
                    w-full  
                    flex
                    justify-center
                    gap-[16px]
                "
            >

                <button
                    className="
                        w-[100px]
                        h-[32px]
                        rounded-full
                        bg-[#808080]
                        font-bold
                    "
                    onClick={onCancel}
                >
                    CANCEL
                </button>

                <button
                    className="
                        w-[100px]
                        h-[32px]
                        rounded-full
                        bg-[#C62828]
                        font-bold
                    "
                    onClick={onConfirm}
                >
                    CLEAR
                </button>

            </div>


        </Panel>

    );

}

export default ClearConfirmationDialog;