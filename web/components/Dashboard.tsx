"use client";

import { useState } from "react";
import { UploadCloud, CheckCircle, AlertTriangle, FileText } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Separator } from "@/components/ui/separator";
import { Badge } from "@/components/ui/badge";
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { ExtractedData, Container, LayoutLine } from "@/types/schema";
import { toast } from "sonner";
import dynamic from "next/dynamic";

const SmartPdfViewer = dynamic(() => import("./SmartPdfViewer").then(mod => mod.SmartPdfViewer), {
    ssr: false,
    loading: () => <div className="h-full flex items-center justify-center bg-gray-100 text-gray-400">Loading Viewer...</div>
});

// Enhanced PDF Viewer with Highlights
const PdfViewer = ({ url, layout }: { url: string | null; layout?: LayoutLine[] }) => {
    if (!url) return <div className="h-full flex items-center justify-center bg-gray-100 text-gray-400">No PDF Loaded</div>;
    return (
        <div className="h-full w-full bg-slate-50 border rounded-lg overflow-hidden relative">
            <SmartPdfViewer url={url} layout={layout} />
        </div>
    );
};

export default function Dashboard() {
    const [fileUrl, setFileUrl] = useState<string | null>(null);
    const [data, setData] = useState<ExtractedData | null>(null);
    const [loading, setLoading] = useState(false);

    const handleFileUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
        const file = e.target.files?.[0];
        if (!file) return;

        setLoading(true);
        // Create local preview URL
        const url = URL.createObjectURL(file);
        setFileUrl(url);

        // Prepare form data
        const formData = new FormData();
        formData.append("file", file);

        try {
            // Call our API (assuming proxy is set up or CORS allowed)
            const res = await fetch("http://localhost:8001/api/v1/parsing/parse", {
                method: "POST",
                body: formData,
            });

            if (!res.ok) throw new Error("Parsing failed");

            const result: ExtractedData = await res.json();
            setData(result);
            toast.success("Document parsed successfully!");
        } catch (error) {
            console.error(error);
            toast.error("Failed to parse document.");
        } finally {
            setLoading(false);
        }
    };

    const handleExportXML = async () => {
        if (!data) return;
        try {
            const res = await fetch("http://localhost:8000/api/v1/parsing/export", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(data),
            });

            if (!res.ok) throw new Error("Export failed");

            // Download file
            const xmlText = await res.json(); // API returns string
            const blob = new Blob([xmlText], { type: "text/xml" });
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement("a");
            a.href = url;
            a.download = "UniversalShipment.xml";
            a.click();
            window.URL.revokeObjectURL(url);

            toast.success("XML Exported!");
        } catch (error) {
            console.error(error);
            toast.error("Failed to export XML.");
        }
    };

    return (
        <div className="h-screen flex flex-col bg-slate-50">
            <header className="bg-white border-b px-6 py-4 flex items-center justify-between shadow-sm">
                <div className="flex items-center gap-2">
                    <span className="text-xl font-bold bg-gradient-to-r from-blue-600 to-indigo-600 bg-clip-text text-transparent">CLOS</span>
                    <Badge variant="outline">v1.0.0</Badge>
                </div>
                <Button variant="outline" size="sm" onClick={handleExportXML} disabled={!data}>
                    Export XML
                </Button>
            </header>

            <main className="flex-1 flex overflow-hidden">
                {/* Left Pane: PDF Viewer */}
                <div className="w-1/2 p-4 h-full border-r bg-white">
                    <PdfViewer url={fileUrl} layout={data?.layout} />
                </div>

                {/* Right Pane: Data Form */}
                <div className="w-1/2 p-4 h-full overflow-y-auto">
                    {!data && !loading && (
                        <div className="h-full flex flex-col items-center justify-center border-2 border-dashed rounded-xl border-slate-300 bg-slate-50/50">
                            <UploadCloud className="h-12 w-12 text-slate-400 mb-4" />
                            <h3 className="text-lg font-semibold text-slate-700">Upload Bill of Lading</h3>
                            <p className="text-sm text-slate-500 mb-6">Drag and drop or click to upload</p>
                            <input type="file" onChange={handleFileUpload} className="hidden" id="file-upload" accept=".pdf" />
                            <label htmlFor="file-upload">
                                <Button asChild>
                                    <span>Select File</span>
                                </Button>
                            </label>
                        </div>
                    )}

                    {loading && (
                        <div className="h-full flex items-center justify-center">
                            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary"></div>
                            <span className="ml-2 text-slate-600">Extracting Data with Gemini 1.5 Flash...</span>
                        </div>
                    )}

                    {data && (
                        <div className="space-y-6">
                            {/* Header Data Card */}
                            <Card>
                                <CardHeader className="pb-2">
                                    <CardTitle className="text-sm font-medium text-slate-500 uppercase">Shipment Header</CardTitle>
                                </CardHeader>
                                <CardContent className="grid grid-cols-2 gap-4">
                                    <div>
                                        <label className="text-xs text-slate-500">Shipper</label>
                                        <div className="font-medium text-sm">{data.header.shipper}</div>
                                    </div>
                                    <div>
                                        <label className="text-xs text-slate-500">Consignee</label>
                                        <div className="font-medium text-sm">{data.header.consignee}</div>
                                    </div>
                                    <div>
                                        <label className="text-xs text-slate-500">SCAC</label>
                                        <div className="font-medium text-sm">{data.header.scac_code}</div>
                                    </div>
                                    <div>
                                        <label className="text-xs text-slate-500">Port of Loading</label>
                                        <div className="font-medium text-sm">{data.header.port_of_loading} ({data.header.pol_locode})</div>
                                    </div>
                                </CardContent>
                            </Card>

                            {/* Containers Table ("The Firewall") */}
                            <Card>
                                <CardHeader className="pb-2">
                                    <div className="flex items-center justify-between">
                                        <CardTitle className="text-sm font-medium text-slate-500 uppercase">Containers & Validation</CardTitle>
                                        <span className="text-xs text-slate-400">ISO 6346 Checksum</span>
                                    </div>
                                </CardHeader>
                                <CardContent className="p-0">
                                    <Table>
                                        <TableHeader>
                                            <TableRow>
                                                <TableHead>Container #</TableHead>
                                                <TableHead>Seal</TableHead>
                                                <TableHead>Checksum</TableHead>
                                            </TableRow>
                                        </TableHeader>
                                        <TableBody>
                                            {data.containers.map((c, i) => (
                                                <TableRow key={i} className={!c.is_valid_checksum ? "bg-red-50" : ""}>
                                                    <TableCell className="font-mono">{c.container_number}</TableCell>
                                                    <TableCell>{c.seal_number}</TableCell>
                                                    <TableCell>
                                                        {c.is_valid_checksum ? (
                                                            <Badge variant="outline" className="bg-green-50 text-green-700 border-green-200">
                                                                <CheckCircle className="w-3 h-3 mr-1" /> Valid
                                                            </Badge>
                                                        ) : (
                                                            <div className="flex items-center text-red-600">
                                                                <AlertTriangle className="w-4 h-4 mr-2" />
                                                                <span className="text-xs font-bold">INVALID</span>
                                                            </div>
                                                        )}
                                                    </TableCell>
                                                </TableRow>
                                            ))}
                                        </TableBody>
                                    </Table>
                                </CardContent>
                            </Card>
                        </div>
                    )}
                </div>
            </main>
        </div>
    );
}
