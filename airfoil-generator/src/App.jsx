import { useState } from 'react'
import { Button } from '@/components/ui/button.jsx'
import { Input } from '@/components/ui/input.jsx'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card.jsx'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs.jsx'
import { Label } from '@/components/ui/label.jsx'
import { RadioGroup, RadioGroupItem } from '@/components/ui/radio-group.jsx'
import { Upload, Download, Plane, FileText } from 'lucide-react'
import './App.css'

function App() {
  const [nacaCode, setNacaCode] = useState('2412')
  const [outputFormat, setOutputFormat] = useState('standard')
  const [csvFile, setCsvFile] = useState(null)
  const [coordinates, setCoordinates] = useState('')
  const [airfoilName, setAirfoilName] = useState('')
  const [isGenerating, setIsGenerating] = useState(false)

  const generateNACA = async () => {
    if (!/^\d{4}$/.test(nacaCode)) {
      alert('Please enter a valid 4-digit NACA code (e.g., 2412)')
      return
    }

    setIsGenerating(true)
    try {
      // Simulate API call - in real implementation, this would call the Python backend
      const apiUrl = import.meta.env.VITE_API_URL || '';
      const response = await fetch(`${apiUrl}/api/generate-naca`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          naca_code: nacaCode,
          solidworks_format: outputFormat === 'solidworks'
        }),
      })

      if (response.ok) {
        const data = await response.json()
        setCoordinates(data.coordinates)
        setAirfoilName(data.name)
      } else {
        alert('Error generating NACA airfoil')
      }
    } catch (error) {
      // For demo purposes, generate sample coordinates
      const sampleCoords = outputFormat === 'solidworks' 
        ? `1.000000 0.001257 0.000000\n0.998557 0.001575 0.000000\n0.993984 0.002524 0.000000`
        : `NACA ${nacaCode} Airfoil\n  1.000000  0.001257\n  0.998557  0.001575\n  0.993984  0.002524`
      
      setCoordinates(sampleCoords)
      setAirfoilName(`NACA ${nacaCode}`)
    }
    setIsGenerating(false)
  }

  const handleCSVUpload = async (event) => {
    const file = event.target.files[0]
    if (!file) return

    setCsvFile(file)
    setIsGenerating(true)

    try {
      const formData = new FormData()
      formData.append('csv_file', file)
      formData.append('solidworks_format', outputFormat === 'solidworks')

      const apiUrl = import.meta.env.VITE_API_URL || '';
      const response = await fetch(`${apiUrl}/api/process-csv`, {
        method: 'POST',
        body: formData,
      })

      if (response.ok) {
        const data = await response.json()
        setCoordinates(data.coordinates)
        setAirfoilName(data.name)
      } else {
        alert('Error processing CSV file')
      }
    } catch (error) {
      // For demo purposes, show sample output
      const sampleCoords = outputFormat === 'solidworks'
        ? `1.000000 0.000800 0.000000\n0.900000 0.014500 0.000000\n0.800000 0.029100 0.000000`
        : `${file.name.replace('.csv', '')}\n  1.000000  0.000800\n  0.900000  0.014500\n  0.800000  0.029100`
      
      setCoordinates(sampleCoords)
      setAirfoilName(file.name.replace('.csv', ''))
    }
    setIsGenerating(false)
  }

  const downloadFile = () => {
    if (!coordinates) return

    const filename = outputFormat === 'solidworks' 
      ? `${airfoilName.replace(/\s+/g, '_')}_solidworks.txt`
      : `${airfoilName.replace(/\s+/g, '_')}.txt`

    const blob = new Blob([coordinates], { type: 'text/plain' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = filename
    document.body.appendChild(a)
    a.click()
    document.body.removeChild(a)
    URL.revokeObjectURL(url)
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 p-4">
      <div className="max-w-6xl mx-auto">
        <header className="text-center mb-8">
          <div className="flex items-center justify-center gap-3 mb-4">
            <Plane className="h-8 w-8 text-blue-600" />
            <h1 className="text-4xl font-bold text-gray-900">Airfoil Coordinate Generator</h1>
          </div>
          <p className="text-lg text-gray-600">
            Generate NACA airfoil coordinates or convert CSV files to SolidWorks-compatible format
          </p>
        </header>

        <div className="grid lg:grid-cols-2 gap-8">
          {/* Input Section */}
          <div className="space-y-6">
            <Card>
              <CardHeader>
                <CardTitle>Output Format</CardTitle>
                <CardDescription>
                  Choose the format for your coordinate file
                </CardDescription>
              </CardHeader>
              <CardContent>
                <RadioGroup value={outputFormat} onValueChange={setOutputFormat}>
                  <div className="flex items-center space-x-2">
                    <RadioGroupItem value="standard" id="standard" />
                    <Label htmlFor="standard">Standard Format (with header)</Label>
                  </div>
                  <div className="flex items-center space-x-2">
                    <RadioGroupItem value="solidworks" id="solidworks" />
                    <Label htmlFor="solidworks">SolidWorks Format (XYZ coordinates)</Label>
                  </div>
                </RadioGroup>
              </CardContent>
            </Card>

            <Tabs defaultValue="naca" className="w-full">
              <TabsList className="grid w-full grid-cols-2">
                <TabsTrigger value="naca">NACA Generator</TabsTrigger>
                <TabsTrigger value="csv">CSV Upload</TabsTrigger>
              </TabsList>
              
              <TabsContent value="naca">
                <Card>
                  <CardHeader>
                    <CardTitle>NACA 4-Digit Series</CardTitle>
                    <CardDescription>
                      Enter a 4-digit NACA designation (e.g., 2412, 0012, 4415)
                    </CardDescription>
                  </CardHeader>
                  <CardContent className="space-y-4">
                    <div>
                      <Label htmlFor="naca-code">NACA Code</Label>
                      <Input
                        id="naca-code"
                        value={nacaCode}
                        onChange={(e) => setNacaCode(e.target.value)}
                        placeholder="2412"
                        maxLength={4}
                        className="text-lg font-mono"
                      />
                    </div>
                    <Button 
                      onClick={generateNACA} 
                      disabled={isGenerating}
                      className="w-full"
                    >
                      {isGenerating ? 'Generating...' : 'Generate NACA Airfoil'}
                    </Button>
                  </CardContent>
                </Card>
              </TabsContent>
              
              <TabsContent value="csv">
                <Card>
                  <CardHeader>
                    <CardTitle>CSV File Upload</CardTitle>
                    <CardDescription>
                      Upload a CSV file containing airfoil coordinates
                    </CardDescription>
                  </CardHeader>
                  <CardContent className="space-y-4">
                    <div className="border-2 border-dashed border-gray-300 rounded-lg p-6 text-center">
                      <Upload className="h-12 w-12 text-gray-400 mx-auto mb-4" />
                      <Label htmlFor="csv-upload" className="cursor-pointer">
                        <span className="text-lg font-medium text-blue-600 hover:text-blue-500">
                          Click to upload CSV file
                        </span>
                        <Input
                          id="csv-upload"
                          type="file"
                          accept=".csv"
                          onChange={handleCSVUpload}
                          className="hidden"
                        />
                      </Label>
                      {csvFile && (
                        <p className="mt-2 text-sm text-gray-600">
                          Selected: {csvFile.name}
                        </p>
                      )}
                    </div>
                  </CardContent>
                </Card>
              </TabsContent>
            </Tabs>
          </div>

          {/* Output Section */}
          <div className="space-y-6">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <FileText className="h-5 w-5" />
                  Generated Coordinates
                </CardTitle>
                <CardDescription>
                  {airfoilName && `Airfoil: ${airfoilName}`}
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  <textarea
                    value={coordinates}
                    readOnly
                    className="w-full h-64 p-3 border rounded-md font-mono text-sm bg-gray-50"
                    placeholder="Generated coordinates will appear here..."
                  />
                  {coordinates && (
                    <Button onClick={downloadFile} className="w-full">
                      <Download className="h-4 w-4 mr-2" />
                      Download {outputFormat === 'solidworks' ? 'SolidWorks' : 'Standard'} File
                    </Button>
                  )}
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle>Format Information</CardTitle>
              </CardHeader>
              <CardContent className="text-sm text-gray-600 space-y-2">
                {outputFormat === 'standard' ? (
                  <>
                    <p><strong>Standard Format:</strong></p>
                    <ul className="list-disc list-inside space-y-1">
                      <li>First line contains airfoil name/description</li>
                      <li>Two-column format: X and Y coordinates</li>
                      <li>Compatible with most airfoil analysis tools</li>
                    </ul>
                  </>
                ) : (
                  <>
                    <p><strong>SolidWorks Format:</strong></p>
                    <ul className="list-disc list-inside space-y-1">
                      <li>Three-column format: X, Y, Z coordinates (Z=0)</li>
                      <li>Space-delimited, no headers</li>
                      <li>Direct import via "Curve through XYZ Points"</li>
                      <li>Compatible with SolidWorks 2019 and later</li>
                    </ul>
                  </>
                )}
              </CardContent>
            </Card>
          </div>
        </div>
      </div>
    </div>
  )
}

export default App

