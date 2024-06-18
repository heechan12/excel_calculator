import streamlit as st
import pandas as pd
import numpy as np


def calculate(values):
    if values:
        try:
            # 입력값을 탭과 개행 문자로 구분하여 리스트로 변환하고 빈 줄을 제거
            data = [list(map(float, filter(None, line.split()))) for line in values.split('\n') if line]

            if data:  # 입력된 숫자가 있을 때만 계산
                # 데이터프레임으로 변환
                df = pd.DataFrame(data, columns=["Channel 1", "Channel 2"])

                # 각 열의 최대값, 평균, 최소값 계산
                metrics = {
                    '항목': ['최대값', '평균', '최소값'],
                }
                for col in df.columns:
                    col_values = df[col]
                    metrics[col] = [
                        f"{col_values.max():.2f}",
                        f"{col_values.mean():.2f}",
                        f"{col_values.min():.2f}",
                    ]

                results_df = pd.DataFrame(metrics)

                # 결과 출력
                st.divider()
                st.subheader("결과")
                st.table(results_df)
            else:
                st.warning("입력된 값이 없습니다. 값을 입력해주세요.")

        except ValueError:
            st.error("잘못된 입력입니다. 각 줄에 숫자를 입력해주세요.")

def main():
    st.title("mVoIP 필드테스트 엑셀 MOS 계산기")

    st.subheader("입력")
    values = st.text_area("연속된 값을 입력하세요 (채널 간 값은 공백, 채널 내 값은 줄 바꿈으로 구분):")

    if st.button("계산하기"):
        calculate(values)


if __name__ == "__main__":
    main()
