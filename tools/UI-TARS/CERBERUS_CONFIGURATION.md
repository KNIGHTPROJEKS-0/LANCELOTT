# UI-TARS Configuration for CERBERUS-FANGS LANCELOTT

## Overview

UI-TARS Desktop has been properly configured for the CERBERUS-FANGS LANCELOTT project with:

- **Primary Model**: Hugging Face UI-TARS-1.5-7B (optimized for GUI automation)
- **Backup Model**: Azure OpenAI GPT-5 (for general AI tasks)
- **Unique Port**: 8765 (to avoid conflicts with other services)
- **Development Mode**: Enabled with debugging

## Quick Start

### Option 1: Using the Startup Script (Recommended)

```bash
./start_ui_tars.sh
```

### Option 2: Manual Start

```bash
cd UI-TARS
npm run dev:ui-tars
```

## Access Points

- **Desktop Application**: Launches automatically
- **Web Interface**: <http://localhost:5173>
- **Internal Port**: 8765 (for UI-TARS communication)

## Configuration Files

### 1. Environment Variables (.env)

- **VLM_PROVIDER**: `huggingface` (UI-TARS-1.5-7B model)
- **VLM_API_KEY**: Your Hugging Face token
- **AZURE_OPENAI_API_KEY**: Your Azure OpenAI key (backup)
- **UI_TARS_PORT**: `8765` (unique port)

### 2. Preset Files

#### cerberus-preset.yaml (Recommended)

- Uses Hugging Face UI-TARS-1.5-7B model
- Optimized for GUI automation tasks
- Better performance for screen interactions

#### cerberus-azure-preset.yaml (Alternative)

- Uses Azure OpenAI GPT-5
- Experimental configuration
- May have limited GUI automation capabilities

## Project Structure

```
UI-TARS/
├── .env                          # Environment configuration
├── cerberus-preset.yaml         # Primary Hugging Face preset
├── cerberus-azure-preset.yaml   # Alternative Azure preset
├── apps/ui-tars/               # Main UI-TARS desktop app
├── packages/                   # Shared packages
└── docs/                      # Documentation
```

## Key Features Configured

1. **Vision-Language Model**: UI-TARS-1.5-7B for GUI understanding
2. **Screen Recording**: Enabled with permission checks
3. **Browser Integration**: Chrome/Safari support
4. **Local Computer Operator**: Direct system control
5. **Screenshot Optimization**: Enabled for better performance

## Troubleshooting

### Common Issues

1. **Permission Errors**: Ensure screen recording and accessibility permissions are granted
2. **Port Conflicts**: UI-TARS uses port 8765, web interface uses 5173
3. **Model Loading**: First run may take time to download UI-TARS model

### Checking Status

- Desktop app logs appear in terminal
- Web interface shows model status
- Check permissions in System Preferences > Privacy & Security

## API Integration Status

✅ **Hugging Face**: Configured with UI-TARS-1.5-7B model
✅ **Azure OpenAI**: Configured as backup (GPT-5)
✅ **OpenAI**: Configured as secondary backup
✅ **Local Computer Control**: Enabled with permissions
✅ **Browser Automation**: Chrome integration active

## Performance Optimization

- Screenshot scale: 1.0 (full resolution)
- Loop interval: 2000ms (balanced performance)
- Max actions per task: 50 (safety limit)
- Action timeout: 30 seconds

## Security Features

- API keys properly configured in .env
- Sandbox mode disabled for system access
- Screen recording permissions enforced
- Local-only operation (no external data sharing)

## Next Steps

1. **Test GUI Automation**: Try simple tasks like opening applications
2. **Configure Browser Tasks**: Set up web automation workflows
3. **Create Custom Presets**: Adjust settings for specific use cases
4. **Monitor Performance**: Check logs for optimization opportunities

## Integration with CERBERUS-FANGS

UI-TARS is now part of the CERBERUS-FANGS toolkit and can be used for:

- Automated penetration testing workflows
- GUI-based security tool interaction
- Screenshot analysis and documentation
- Automated report generation
- Cross-platform desktop automation

## Support

- Official Documentation: <https://github.com/bytedance/UI-TARS-desktop>
- Model Information: <https://huggingface.co/bytedance-research/UI-TARS-1.5-7B>
- CERBERUS-FANGS Integration: See main project documentation
