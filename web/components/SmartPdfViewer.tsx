"use client";

import React, { useState, useEffect } from "react";
import {
    PdfLoader,
    PdfHighlighter,
    TextHighlight,
    MonitoredHighlightContainer,
    useHighlightContainerContext,
    Highlight
} from "react-pdf-highlighter-extended";
import "react-pdf-highlighter-extended/dist/esm/style/PdfHighlighter.css";
import "react-pdf-highlighter-extended/dist/esm/style/AreaHighlight.css";

// Interface for our custom highlight with comment
interface MyHighlight extends Highlight {
    comment: { text: string; emoji: string };
}

// import "react-pdf-highlighter-extended/dist/esm/style/TextHighlight.css";

import { LayoutLine } from "@/types/schema";

// Helper to manually set worker if needed, though PdfLoader has a prop for it.
// We will pass it via PdfLoader prop.

interface Props {
    url: string;
    layout: LayoutLine[] | undefined;
}

const HighlightPopup = ({
    comment,
}: {
    comment: { text: string; emoji: string };
}) => (
    comment.text ? (
        <div className="bg-white border text-xs p-2 rounded shadow-md z-50">
            {comment.emoji} {comment.text}
        </div>
    ) : null
);

// Component that renders an individual highlight using Context
const HighlightComponent = () => {
    const { highlight, isScrolledTo } = useHighlightContainerContext<MyHighlight>();

    const component = (
        <TextHighlight
            isScrolledTo={isScrolledTo}
            highlight={highlight}
        />
    );

    const highlightTip = {
        position: highlight.position,
        content: <HighlightPopup comment={highlight.comment} />
    };

    return (
        <MonitoredHighlightContainer
            highlightTip={highlightTip}
        >
            {component}
        </MonitoredHighlightContainer>
    );
};

export function SmartPdfViewer({ url, layout }: Props) {
    const [highlights, setHighlights] = useState<any[]>([]);

    useEffect(() => {
        if (layout) {
            // Map Backend Normalized Layout to Highlight Format
            const mapped = layout.map((l, i) => {
                return {
                    id: i.toString(),
                    type: "text",
                    comment: { text: l.text, emoji: "🔍" },
                    content: { text: l.text },
                    position: {
                        boundingRect: {
                            x1: l.bbox.x,
                            y1: l.bbox.y,
                            x2: l.bbox.x + l.bbox.width,
                            y2: l.bbox.y + l.bbox.height,
                            width: l.bbox.width,
                            height: l.bbox.height,
                            pageNumber: 1,
                        },
                        rects: [
                            {
                                x1: l.bbox.x,
                                y1: l.bbox.y,
                                x2: l.bbox.x + l.bbox.width,
                                y2: l.bbox.y + l.bbox.height,
                                width: l.bbox.width,
                                height: l.bbox.height,
                                pageNumber: 1,
                            },
                        ],
                        pageNumber: 1,
                        usePdfCoordinates: false, // Critical based on our normalization
                    },
                };
            });
            setHighlights(mapped);
        }
    }, [layout]);

    return (
        <div className="h-full relative bg-slate-100 overflow-hidden">
            <PdfLoader
                document={url}
                beforeLoad={(progress) => <div className="p-4">Loading PDF...</div>}
                workerSrc={`//unpkg.com/pdfjs-dist@4.10.38/build/pdf.worker.min.mjs`}
            >
                {(pdfDocument) => (
                    <PdfHighlighter
                        pdfDocument={pdfDocument}
                        enableAreaSelection={(event) => event.altKey}
                        highlights={highlights}
                        utilsRef={() => { }}
                    >
                        <HighlightComponent />
                    </PdfHighlighter>
                )}
            </PdfLoader>
        </div>
    );
}
