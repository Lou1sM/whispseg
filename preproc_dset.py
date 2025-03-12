import os
from pydub import AudioSegment
import pandas as pd
import shutil


def convert_our_df_to_theirs(df):
    ddict = {
             'onset': df['Begin Time (s)'],
             'offset': df['End Time (s)'],
             'cluster': df['Annotation']
             }
    return pd.DataFrame(ddict, index=df.index)


def convert_their_df_to_ours(df):
    if len(df)==0:
        return pd.DataFrame(columns=['Begin Time (s)', 'End Time (s)', 'Annotation', 'Detection Prob', 'Class Prob'])
    else:
        ddict = {
                 'Begin Time (s)': df['onset'],
                 'End Time (s)': df['offset'],
                 'Annotation': df['cluster']
                 }
        ddict = {
                 'Begin Time (s)': df['onset'],
                 'End Time (s)': df['offset'],
                 'Annotation': df['cluster']
                 }
        df = pd.DataFrame(ddict, index=df.index)
        df['Detection Prob'] = 1
        df['Class Prob'] = 1
        return df

if __name__ == '__main__':
    #dset = 'MT'
    #for dset in ['Anuraset', 'BV_slowed', 'hawaii', 'humpback', 'katydids_slowed', 'MT', 'powdermill', 'OZF_slowed']:
    for dset in ['OZF_slowed']:
        for split in ('train', 'test'):
            os.makedirs(out_dir:=f'data/ours/{dset}/{split}', exist_ok=True)
            in_dir = f'../vb3/datasets/{dset}/formatted'
            split_info = pd.read_csv(f'{in_dir}/{split}_info.csv')
            for i, row in split_info.iterrows():
                #assert row.audio_fp == row.selection_table_fp.replace('.txt', '.wav').replace('/selection_tables/', '/audio/')
                st_fn = os.path.basename(row.selection_table_fp)
                audio_fn = os.path.basename(row.audio_fp)
                in_df = pd.read_csv(f'{in_dir}/selection_tables/{st_fn}', sep='\t')
                out_df = convert_our_df_to_theirs(in_df)
                out_df.to_csv(f'{out_dir}/{st_fn}'.replace('.txt', '.csv'))
                #shutil.copyfile(f'{in_dir}/audio/{audio_fn}', f'{out_dir}/{audio_fn}')
                curr_audio_fp = os.path.abspath(f'../vb3/{row.audio_fp}')
                new_audio_fp = os.path.abspath(f'{out_dir}/{st_fn}'.replace('.txt', '.wav'))
                assert os.path.exists(curr_audio_fp)
                if os.path.lexists(new_audio_fp):
                    os.remove(new_audio_fp)
                if curr_audio_fp.endswith('.wav'):
                    os.symlink(curr_audio_fp, new_audio_fp)
                else: # just OZF I thin
                    audio = AudioSegment.from_file(curr_audio_fp, format="flac")
                    audio.export(new_audio_fp, format="wav")

