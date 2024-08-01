from chapter_20.flags import save_flag, get_flag, main


def downloader(cc_lst: list[str]) -> int:  # 3.89 sec.

    for cc in cc_lst:
        cc_img = get_flag(cc=cc)
        save_flag(img_data=cc_img, filename=f"{cc}.gif")

        print(cc, end=" ", flush=True)

    return len(cc_lst)


if __name__ == "__main__":
    main(downloader=downloader)
