import streamlit as st
import pandas as pd


def main():
    st.title("필드테스트 엑셀 계산기")

    st.subheader("입력")
    values = st.text_area("연속된 값을 입력하세요 (각 값은 줄 바꿈으로 구분):")

    if values:
        try:
            # 입력값을 개행 문자로 구분하여 리스트로 변환하고 빈 줄을 제거
            numbers = list(map(float, filter(None, values.split('\n'))))

            if numbers:  # 입력된 숫자가 있을 때만 계산
                # 평균 계산
                average = round(sum(numbers) / len(numbers), 2)

                # 최대값 계산
                maximum = round(max(numbers), 2)

                # 최소값 계산
                minimum = round(min(numbers), 2)

                # 결과를 데이터프레임으로 저장
                results = {
                    'Metric': ['최대값', '평균', '최소값'],
                    'Value': [f"{maximum:.2f}", f"{average:.2f}", f"{minimum:.2f}"]
                }
                results_df = pd.DataFrame(results)

                # 결과 출력
                st.divider()
                st.subheader("결과")
                st.table(results_df)
            else:
                st.warning("입력된 값이 없습니다. 값을 입력해주세요.")

        except ValueError:
            st.error("잘못된 입력입니다. 각 줄에 숫자를 입력해주세요.")


if __name__ == "__main__":
    main()