import type { SidebarsConfig } from '@docusaurus/plugin-content-docs';

const sidebars: SidebarsConfig = {

  documentationSidebar: [
    'index',
    'installation',
    'app-performance-issues',
    {
      type: 'category',
      label: '控件',
      collapsed: true,
      items: [
        'controls/mediaplayer',
        'controls/messagebox',
        'controls/numericupdown',
        'controls/pdfviewer',
        'controls/richtexteditor',
      ],
    },
    {
      type: 'category',
      label: '平台相关问题',
      collapsed: true,
      items: [
        'platform-specific-issues/macos',
        'platform-specific-issues/webassembly',
        'platform-specific-issues/windows'
      ],
    },
    {
      type: 'category',
      label: '工具',
      collapsed: true,
      items: [
        'tools/developer-tools'
      ],
    },
    {
      type: 'category',
      label: '界面开发',
      collapsed: true,
      items: [
        'ui-development/styles',
        'ui-development/themes'
      ],
    },
    'login-issues',
  ],
};

export default sidebars;
