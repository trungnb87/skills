import React from 'react';
import {Composition} from 'remotion';
import {MapRoute, MapProps} from './MapRoute';
export const RemotionRoot: React.FC = () => (
  <Composition id="MapRoute" component={MapRoute as any} width={1080} height={1920} fps={30} durationInFrames={240}
    defaultProps={{} as MapProps}
    calculateMetadata={({props}: any) => ({durationInFrames: props.durationInFrames ?? 240, fps: props.fps ?? 30})} />
);
